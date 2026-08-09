#!/usr/bin/env python3
"""Fix broken vault wikilinks in content folders and .audit/."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---", re.DOTALL)
SCALAR_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
# [[target]] or [[target|alias]] - skip embeds ![[...]]
WIKILINK_RE = re.compile(r"(?<!!)\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]")

LINK_FOLDERS = (
    "calendar",
    "career",
    "documents",
    "finance",
    "health",
    "internet",
    "manual",
    "media",
    "sensors",
    "social",
    "statistics",
    "wiki",
    ".audit",
)


def vault_root() -> Path:
    # scripts/ -> brain-init/ -> skills/ -> .cursor/ -> vault root
    return Path(__file__).resolve().parents[4]


def normalize(name: str) -> str:
    text = name.strip().lower()
    text = text.replace(".md", "")
    text = re.sub(r"[_\-/]+", " ", text)
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_title(text: str) -> str | None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    for raw in match.group(1).splitlines():
        m = SCALAR_RE.match(raw.rstrip())
        if not m or m.group(1) != "title":
            continue
        value = m.group(2).strip()
        if (value.startswith("'") and value.endswith("'")) or (
            value.startswith('"') and value.endswith('"')
        ):
            return value[1:-1]
        return value or None
    return None


@dataclass
class Note:
    path: Path
    rel: str
    stem: str
    title: str | None
    folder: str
    text: str


@dataclass
class Report:
    fixed: list[str] = field(default_factory=list)
    unresolved: list[str] = field(default_factory=list)
    skipped_ambiguous: list[str] = field(default_factory=list)


def load_notes(root: Path) -> list[Note]:
    notes: list[Note] = []
    for folder in LINK_FOLDERS:
        base = root / folder
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            notes.append(
                Note(
                    path=path,
                    rel=path.relative_to(root).as_posix(),
                    stem=path.stem,
                    title=parse_title(text),
                    folder=folder,
                    text=text,
                )
            )
    return notes


def build_indexes(notes: list[Note]) -> tuple[dict[str, Note], dict[str, list[Note]]]:
    by_stem: dict[str, Note] = {}
    by_norm: dict[str, list[Note]] = {}
    for note in notes:
        by_stem[note.stem] = note
        keys = {normalize(note.stem)}
        if note.title:
            keys.add(normalize(note.title))
        for key in keys:
            if not key:
                continue
            by_norm.setdefault(key, []).append(note)
    for key, vals in by_norm.items():
        seen: set[str] = set()
        uniq: list[Note] = []
        for n in vals:
            if n.rel in seen:
                continue
            seen.add(n.rel)
            uniq.append(n)
        by_norm[key] = uniq
    return by_stem, by_norm


def resolve_target(
    target: str,
    by_stem: dict[str, Note],
    by_norm: dict[str, list[Note]],
) -> tuple[Note | None, str]:
    """Return (note, status) where status is ok|fixed|missing|ambiguous."""
    raw = target.strip()
    if not raw:
        return None, "missing"

    if "/" in raw or raw.endswith(".md"):
        stem = Path(raw).stem
        if stem in by_stem:
            return by_stem[stem], ("ok" if stem == raw or raw.endswith(stem + ".md") else "fixed")
        raw = stem

    if raw in by_stem:
        return by_stem[raw], "ok"

    candidates = by_norm.get(normalize(raw), [])
    if len(candidates) == 1:
        return candidates[0], "fixed"
    if len(candidates) > 1:
        return None, "ambiguous"
    return None, "missing"


def rewrite_wikilinks(
    note: Note,
    by_stem: dict[str, Note],
    by_norm: dict[str, list[Note]],
    report: Report,
) -> str:
    text = note.text

    def repl(match: re.Match[str]) -> str:
        target = match.group(1).strip()
        alias = match.group(2)
        resolved, status = resolve_target(target, by_stem, by_norm)
        if status == "ok":
            return match.group(0)
        if status == "fixed" and resolved is not None:
            new_target = resolved.stem
            if new_target == target:
                return match.group(0)
            report.fixed.append(f"{note.rel}: [[{target}]] → [[{new_target}]]")
            if alias is not None:
                return f"[[{new_target}|{alias}]]"
            return f"[[{new_target}]]"
        if status == "ambiguous":
            report.skipped_ambiguous.append(f"{note.rel}: [[{target}]]")
            return match.group(0)
        report.unresolved.append(f"{note.rel}: [[{target}]]")
        return match.group(0)

    return WIKILINK_RE.sub(repl, text)


def run(root: Path, apply: bool) -> Report:
    notes = load_notes(root)
    by_stem, by_norm = build_indexes(notes)
    report = Report()
    texts: dict[str, str] = {}

    for note in notes:
        texts[note.rel] = rewrite_wikilinks(note, by_stem, by_norm, report)

    if apply:
        for note in notes:
            new_text = texts[note.rel]
            if new_text != note.text:
                note.path.write_text(new_text, encoding="utf-8")

    report.unresolved = sorted(set(report.unresolved))
    report.skipped_ambiguous = sorted(set(report.skipped_ambiguous))
    return report


def print_report(report: Report) -> None:
    print(f"Fixed broken links: {len(report.fixed)}")
    for item in report.fixed:
        print(f"  {item}")
    print(f"Unresolved broken links: {len(report.unresolved)}")
    for item in report.unresolved:
        print(f"  {item}")
    if report.skipped_ambiguous:
        print(f"Ambiguous (skipped): {len(report.skipped_ambiguous)}")
        for item in report.skipped_ambiguous:
            print(f"  {item}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Fix broken wikilinks in content folders and .audit/."
        )
    )
    parser.add_argument(
        "--root",
        type=Path,
        help="Vault root (default: infer from script location)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report changes without writing files",
    )
    args = parser.parse_args()
    root = args.root.resolve() if args.root else vault_root()
    report = run(root, apply=not args.dry_run)
    print_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
