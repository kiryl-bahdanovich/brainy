#!/usr/bin/env python3
"""Remove leftover vault INDEX.md / folder index.md inventories; optional stdout report."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---", re.DOTALL)
SCALAR_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")

IGNORE_DIRS = {".git", ".obsidian", ".trash", ".DS_Store", "__pycache__"}
IGNORE_FILES = {".DS_Store", ".gitkeep", "INDEX.md", "index.md", "AGENTS.md"}

# Content folders: role blurbs + counts (full file lists only with --full).
CONTENT_ROLES = {
    "calendar": "schedule exports, events, time blocks",
    "career": "work, brand, business: reviews, offers, content drafts, consulting pipeline",
    "documents": "books, contracts, and other documents (PDFs, scans)",
    "finance": "income, expenses, statements, money exports",
    "health": "medical records, nutrition log",
    "internet": "saved web articles and excerpts",
    "manual": "hand-written notes and journals",
    "media": "photos, audio, and other media",
    "sensors": "wearable and personal sensor device data / exports",
    "social": "people, relationships, messages and social context",
    "statistics": "external reports and datasets (PDFs, spreadsheets)",
}

ROOT_DOCS = ("AGENTS.md", "CLAUDE.md")
SCRIPT_PATH = "python3 .cursor/skills/brain-init/scripts/cleanup_indexes.py"


def vault_root() -> Path:
    # scripts/ -> brain-init/ -> skills/ -> .cursor/ -> vault root
    return Path(__file__).resolve().parents[4]


def parse_frontmatter(text: str) -> dict | None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None

    data: dict = {}
    current_list_key: str | None = None
    current_fold_key: str | None = None
    fold_parts: list[str] = []

    def flush_fold() -> None:
        nonlocal current_fold_key, fold_parts
        if current_fold_key is None:
            return
        data[current_fold_key] = " ".join(fold_parts).strip()
        current_fold_key = None
        fold_parts = []

    for raw in match.group(1).splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue

        # Continuation of folded/literal block (indented, not a list item key)
        if current_fold_key is not None:
            if re.match(r"^\s+\S", line) and not SCALAR_RE.match(line.lstrip()):
                fold_parts.append(line.strip())
                continue
            flush_fold()

        if current_list_key and re.match(r"^\s+-\s+", line):
            item = re.sub(r"^\s+-\s+", "", line).strip().strip("'\"")
            data.setdefault(current_list_key, []).append(item)
            continue

        current_list_key = None
        m = SCALAR_RE.match(line)
        if not m:
            continue

        key, value = m.group(1), m.group(2).strip()
        if value in ("", "|", ">", ">-", "|-"):
            if value in (">", ">-", "|", "|-"):
                current_fold_key = key
                fold_parts = []
                data[key] = ""
            else:
                current_list_key = key
                data[key] = []
            continue

        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = (
                []
                if not inner
                else [part.strip().strip("'\"") for part in inner.split(",")]
            )
            continue

        if (value.startswith("'") and value.endswith("'")) or (
            value.startswith('"') and value.endswith('"')
        ):
            data[key] = value[1:-1]
            continue

        data[key] = value

    flush_fold()
    return data


def skill_blurb(skill_md: Path) -> tuple[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    fm = parse_frontmatter(text) or {}
    name = str(fm.get("name") or skill_md.parent.name)
    desc = str(fm.get("description") or "").strip()
    # description may be folded YAML; take first sentence-ish line
    desc = re.sub(r"\s+", " ", desc).strip()
    if len(desc) > 120:
        desc = desc[:117].rstrip() + "..."
    return name, desc


def list_files(folder: Path) -> list[Path]:
    files: list[Path] = []
    if not folder.is_dir():
        return files
    for path in sorted(folder.rglob("*")):
        if not path.is_file():
            continue
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.name in IGNORE_FILES:
            continue
        files.append(path)
    return files


def fm_suffix(path: Path) -> str:
    if path.suffix.lower() != ".md":
        return ""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return ""
    fm = parse_frontmatter(text)
    if not fm:
        return ""

    tags = fm.get("tags") or fm.get("state") or []
    if isinstance(tags, str):
        tags = [tags]
    categories = fm.get("categories") or []
    if isinstance(categories, str):
        categories = [categories]
    status = fm.get("status") or fm.get("state")
    parts = []
    if fm.get("title"):
        parts.append(f"title: {fm['title']}")
    if status:
        parts.append(f"status: {status}" if "status" in fm else f"state: {status}")
    if tags and "tags" in fm:
        parts.append("tags: " + ", ".join(str(t) for t in tags))
    elif tags and "state" in fm and "status" not in fm:
        pass
    if categories:
        parts.append("categories: " + ", ".join(str(c) for c in categories))
    if fm.get("task_type"):
        parts.append(f"task: {fm['task_type']}")
    waste = fm.get("waste") or []
    if isinstance(waste, str):
        waste = [waste]
    if waste:
        parts.append("waste: " + ", ".join(str(w) for w in waste))
    if fm.get("steps_total") is not None and str(fm.get("steps_total")).strip() != "":
        wasted = str(fm.get("steps_wasted", "0")).strip() or "0"
        parts.append(f"steps: {fm['steps_total']} ({wasted} wasted)")
    if fm.get("mood") is not None and str(fm.get("mood")).strip() != "":
        parts.append(f"mood: {fm['mood']}")
    if fm.get("created"):
        parts.append(f"created: {fm['created']}")
    if not parts:
        return ""
    return " - " + " | ".join(parts)


def render_tree(folder: Path) -> list[str]:
    lines: list[str] = []
    files = list_files(folder)
    if not files:
        lines.append("_empty_")
        return lines

    for path in files:
        rel = path.relative_to(folder).as_posix()
        # Clickable relative link (Obsidian / GitHub preview), not orphan backticks
        lines.append(f"- [{rel}](./{rel}){fm_suffix(path)}")
    return lines


def content_folder_names(root: Path) -> list[str]:
    top_dirs = [
        p.name
        for p in sorted(root.iterdir())
        if p.is_dir() and p.name not in IGNORE_DIRS and not p.name.startswith(".")
    ]
    ordered = [d for d in CONTENT_ROLES if d in top_dirs]
    ordered += [d for d in top_dirs if d not in CONTENT_ROLES]
    return ordered


def render_content_folders(root: Path, *, full: bool) -> list[str]:
    lines: list[str] = [
        "## Content folders",
        "",
    ]
    if not full:
        lines.append(
            "Counts only - discovery is skill `brain-search` (hub + frontmatter). "
            "Vault `INDEX.md` / folder `index.md` inventories are not maintained. "
            "Pass `--full` to `cleanup_indexes.py` for an inline complete dump."
        )
        lines.append("")

    for name in content_folder_names(root):
        folder = root / name
        role = CONTENT_ROLES.get(name, "vault content")
        files = list_files(folder)
        lines.append(f"### `{name}/`")
        lines.append("")
        lines.append(f"{role} - **{len(files)}** file(s)")
        lines.append("")
        if full:
            lines.extend(render_tree(folder))
            lines.append("")
        else:
            if not files:
                lines.append("_empty_")
            elif len(files) <= 12:
                lines.extend(render_tree(folder))
            else:
                lines.append(
                    f"_file list omitted ({len(files)} files) - re-run with `--full`_"
                )
            lines.append("")

    return lines


def render_skills(root: Path) -> list[str]:
    skills_root = root / ".cursor" / "skills"
    lines: list[str] = ["## Skills (`.cursor/skills/`)", ""]
    if not skills_root.is_dir():
        lines.append("_no skills directory_")
        lines.append("")
        return lines

    for skill_dir in sorted(p for p in skills_root.iterdir() if p.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            lines.append(f"- `{skill_dir.name}/` - (no SKILL.md)")
            continue
        name, desc = skill_blurb(skill_md)
        scripts = skill_dir / "scripts"
        script_note = ""
        if scripts.is_dir():
            script_files = sorted(p.name for p in scripts.iterdir() if p.is_file())
            if script_files:
                script_note = " | scripts: " + ", ".join(f"`{s}`" for s in script_files)
        blurb = f" - {desc}" if desc else ""
        lines.append(f"- `{name}`{blurb}{script_note}")

    lines.append("")
    return lines


def is_index_inventory_name(name: str) -> bool:
    """True for INDEX.md / index.md / *-INDEX.md / '* - INDEX.md' leftovers."""
    if name in {"INDEX.md", "index.md"}:
        return True
    lower = name.casefold()
    return lower.endswith("-index.md") or lower.endswith(" - index.md")


def remove_index_files(root: Path) -> list[str]:
    """Delete root/folder index inventories and leftover *-INDEX.md lists."""
    removed: list[str] = []
    # Root vault index (no longer maintained).
    for name in ("INDEX.md", "index.md"):
        path = root / name
        if path.is_file():
            path.unlink()
            removed.append(path.relative_to(root).as_posix())

    scan_dirs = [root / name for name in content_folder_names(root)]
    audit = root / ".audit"
    if audit.is_dir():
        scan_dirs.append(audit)

    for folder in scan_dirs:
        if not folder.is_dir():
            continue
        for path in folder.iterdir():
            if not path.is_file():
                continue
            if not is_index_inventory_name(path.name):
                continue
            path.unlink()
            removed.append(path.relative_to(root).as_posix())

    return removed


def render_navigation_report(root: Path, *, full: bool = False) -> str:
    """Stdout-only navigation report. Does not write index files."""
    today = date.today().isoformat()
    lines: list[str] = [
        "# Vault navigation report",
        "",
        f"> Generated on {today} by skill `brain-init` (`{SCRIPT_PATH}`). "
        "Stdout only - vault index inventories are not written.",
        "",
        "Navigation is **folder hubs** (each content folder's `AGENTS.md`) plus "
        "skill `brain-search` (frontmatter). Vault `INDEX.md` / folder "
        "`index.md` inventories are not maintained. Full folder dumps are opt-in "
        "(`--full`).",
        "",
        "## Root agent docs",
        "",
    ]

    for name in ROOT_DOCS:
        path = root / name
        mark = "✓" if path.is_file() else "missing"
        lines.append(f"- `{name}` - {mark}")

    lines.append("")
    lines.extend(render_content_folders(root, full=full))
    lines.extend(render_skills(root))
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Remove leftover root INDEX.md / folder index.md and *-INDEX.md "
            "inventories. Does not write new index files. "
            "Use --stdout to print a navigation report without writing."
        )
    )
    parser.add_argument(
        "--root",
        type=Path,
        help="Vault root (default: infer from script location)",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Include complete per-folder file lists in --stdout report",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print a navigation report to stdout (does not write index files)",
    )
    args = parser.parse_args()

    root = args.root.resolve() if args.root else vault_root()

    if args.stdout:
        print(render_navigation_report(root, full=args.full), end="")
        return 0

    removed = remove_index_files(root)
    if removed:
        for rel in removed:
            print(f"Removed {rel}")
    else:
        print("No index files to remove")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
