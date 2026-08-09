#!/usr/bin/env python3
"""Search vault notes by hub (content folder) + YAML frontmatter only.

Matching never uses markdown body text. Optional --hub / --folder scopes to
one or more personal data folders before scanning all hubs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---", re.DOTALL)
SCALAR_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")

# Content-folder hubs (must match on-disk personal data folders)
CONTENT_HUBS = (
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
)

SKIP_NAMES = frozenset({"AGENTS.md", "CLAUDE.md", "INDEX.md", "index.md"})


def vault_root() -> Path:
    # scripts/ -> brain-search/ -> skills/ -> .cursor/ -> vault root
    return Path(__file__).resolve().parents[4]


def parse_frontmatter(text: str) -> dict | None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None

    data: dict = {}
    current_list_key: str | None = None

    for raw in match.group(1).splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue

        if current_list_key and re.match(r"^\s+-\s+", line):
            item = re.sub(r"^\s+-\s+", "", line).strip().strip("'\"")
            data.setdefault(current_list_key, []).append(item)
            continue

        current_list_key = None
        m = SCALAR_RE.match(line)
        if not m:
            continue

        key, value = m.group(1), m.group(2).strip()
        if value == "" or value == "|" or value == ">":
            current_list_key = key
            data[key] = []
            continue

        if (value.startswith("[") and value.endswith("]")) or (
            value.startswith("'") and value.endswith("'")
        ) or (value.startswith('"') and value.endswith('"')):
            if value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                if not inner:
                    data[key] = []
                else:
                    data[key] = [
                        part.strip().strip("'\"") for part in inner.split(",")
                    ]
            else:
                data[key] = value[1:-1]
            continue

        data[key] = value

    return data


def searchable_blob(path: Path, fm: dict, root: Path) -> str:
    tags = fm.get("tags") or []
    if isinstance(tags, str):
        tags = [tags]
    try:
        rel = path.relative_to(root).as_posix()
    except ValueError:
        rel = path.as_posix()
    parts = [
        path.name,
        path.stem,
        rel,
        str(fm.get("title", "")),
        str(fm.get("description", "")),
        str(fm.get("status", "")),
        str(fm.get("created", "")),
        str(fm.get("source", "")),
        " ".join(str(t) for t in tags),
    ]
    return " ".join(parts).lower()


def normalize_hubs(names: list[str]) -> list[str]:
    """Map --hub / --folder names to known content hubs (case-insensitive)."""
    out: list[str] = []
    for name in names:
        cleaned = name.strip().strip("/")
        canon = next(
            (h for h in CONTENT_HUBS if h.casefold() == cleaned.casefold()),
            None,
        )
        if canon is None:
            print(
                f"warn: unknown hub '{name}' "
                f"(known: {', '.join(CONTENT_HUBS)})",
                file=sys.stderr,
            )
            continue
        if canon not in out:
            out.append(canon)
    return out


def iter_notes(root: Path, hubs: list[str]) -> list[Path]:
    notes: list[Path] = []
    for hub in hubs:
        base = root / hub
        if not base.is_dir():
            print(f"warn: hub missing on disk: {hub}/", file=sys.stderr)
            continue
        for path in sorted(base.rglob("*.md")):
            if path.name in SKIP_NAMES:
                continue
            notes.append(path)
    return notes


def matches(
    path: Path,
    fm: dict,
    root: Path,
    query_terms: list[str],
    tags: list[str],
    status: str | None,
) -> bool:
    if status and str(fm.get("status", "")).lower() != status.lower():
        return False

    note_tags = fm.get("tags") or []
    if isinstance(note_tags, str):
        note_tags = [note_tags]
    note_tags_l = {str(t).lower() for t in note_tags}
    for tag in tags:
        if tag.lower() not in note_tags_l:
            return False

    if not query_terms:
        return True

    blob = searchable_blob(path, fm, root)
    return all(term.lower() in blob for term in query_terms)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Search content-folder hubs by YAML frontmatter only "
            "(no body matching)."
        )
    )
    parser.add_argument(
        "query",
        nargs="*",
        help=(
            "Terms matched against title, description, tags, status, "
            "created, source, filename"
        ),
    )
    parser.add_argument(
        "--hub",
        action="append",
        default=[],
        metavar="NAME",
        help=(
            "Limit to content-folder hub (repeatable). "
            f"Known: {', '.join(CONTENT_HUBS)}"
        ),
    )
    parser.add_argument(
        "--tag",
        action="append",
        default=[],
        help="Require tag (repeatable)",
    )
    parser.add_argument(
        "--status",
        choices=["draft", "active", "archived"],
        help="Filter by status",
    )
    parser.add_argument(
        "--folder",
        action="append",
        default=[],
        metavar="NAME",
        help="Alias for --hub (repeatable)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON array instead of text lines",
    )
    parser.add_argument(
        "--root",
        type=Path,
        help="Vault root (default: infer from script location)",
    )
    args = parser.parse_args()

    root = args.root.resolve() if args.root else vault_root()
    scoped = normalize_hubs(list(args.hub) + list(args.folder))
    hubs = scoped or list(CONTENT_HUBS)

    candidates = iter_notes(root, hubs)
    results = []

    for path in candidates:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"warn: skip {path}: {exc}", file=sys.stderr)
            continue

        fm = parse_frontmatter(text)
        if fm is None:
            continue

        if not matches(path, fm, root, args.query, args.tag, args.status):
            continue

        rel = path.relative_to(root).as_posix()
        tags = fm.get("tags") or []
        if isinstance(tags, str):
            tags = [tags]

        item = {
            "path": rel,
            "title": fm.get("title"),
            "description": fm.get("description"),
            "status": fm.get("status"),
            "tags": tags,
            "created": fm.get("created"),
        }
        if fm.get("source") is not None:
            item["source"] = fm.get("source")
        results.append(item)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        if not results:
            print("No matches.")
            return 0
        for item in results:
            tags = ", ".join(item["tags"]) if item["tags"] else "-"
            source = item.get("source")
            source_bit = f" | source: {source}" if source else ""
            print(
                f"{item['path']}\n"
                f"  title: {item['title']}\n"
                f"  description: {item['description']}\n"
                f"  status: {item['status']} | tags: {tags} | "
                f"created: {item['created']}{source_bit}\n"
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
