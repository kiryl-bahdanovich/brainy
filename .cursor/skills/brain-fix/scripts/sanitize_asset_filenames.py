#!/usr/bin/env python3
"""Sanitize content-folder filenames (no spaces) and rewrite markdown references.

Renames files under personal data folders whose names contain spaces
(whitespace -> '-', collapse repeats). Does not rename `.audit/` notes.
Then rewrites occurrences of old names across vault Markdown (content folders,
`.audit/` bodies, root docs). Skips skill/plan example text.
Usage (from vault root):
  python3 .cursor/skills/brain-fix/scripts/sanitize_asset_filenames.py
  python3 .cursor/skills/brain-fix/scripts/sanitize_asset_filenames.py --dry-run
"""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

ASSET_FOLDERS = (
    "calendar",
    "career",
    "documents",
    "finance",
    "health",
    "internet",
    "manual",
    "media",
    "social",
    "statistics",
)
SKIP_DIR_PARTS = {".git", ".obsidian", ".trash", "__pycache__"}


def vault_root() -> Path:
    # scripts/ -> brain-fix/ -> skills/ -> .cursor/ -> vault root
    return Path(__file__).resolve().parents[4]


def sanitize_name(name: str) -> str:
    if "." in name:
        stem, ext = name.rsplit(".", 1)
        ext = "." + ext
    else:
        stem, ext = name, ""
    new_stem = re.sub(r"\s+", "-", stem)
    new_stem = re.sub(r"-{2,}", "-", new_stem).strip("-")
    return new_stem + ext


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIR_PARTS for part in path.parts)


def git_tracked(root: Path, path: Path) -> bool:
    r = subprocess.run(
        ["git", "ls-files", "--error-unmatch", str(path.relative_to(root))],
        cwd=root,
        capture_output=True,
    )
    return r.returncode == 0


def rename_path(root: Path, src: Path, dest: Path, *, dry_run: bool) -> None:
    rel_src = src.relative_to(root).as_posix()
    rel_dest = dest.relative_to(root).as_posix()
    if dry_run:
        print(f"would rename: {rel_src} -> {rel_dest}")
        return
    if git_tracked(root, src):
        r = subprocess.run(
            ["git", "mv", "--", str(src), str(dest)],
            cwd=root,
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            src.rename(dest)
            print(f"git mv failed, fs rename: {rel_src} -> {rel_dest}")
        else:
            print(f"git mv: {rel_src} -> {rel_dest}")
    else:
        src.rename(dest)
        print(f"rename: {rel_src} -> {rel_dest}")


def collect_renames(root: Path) -> list[tuple[Path, Path, str, str]]:
    """Return list of (src, dest, old_name, new_name)."""
    planned: list[tuple[Path, Path, str, str]] = []
    for folder_name in ASSET_FOLDERS:
        folder = root / folder_name
        if not folder.is_dir():
            continue
        for path in sorted(folder.rglob("*")):
            if not path.is_file() or is_skipped(path):
                continue
            if " " not in path.name:
                continue
            new_name = sanitize_name(path.name)
            if new_name == path.name:
                continue
            dest = path.with_name(new_name)
            planned.append((path, dest, path.name, new_name))
    return planned


def rewrite_text(text: str, replacements: list[tuple[str, str]]) -> tuple[str, int]:
    """Replace old filenames with new ones (longest first). Returns (text, count)."""
    count = 0
    for old, new in replacements:
        if old == new:
            continue
        if old not in text:
            continue
        n = text.count(old)
        text = text.replace(old, new)
        count += n
    return text, count


def iter_markdown_for_rewrite(root: Path):
    """Markdown where filename refs should be updated (not code/docs with examples)."""
    allow_files = {
        root / "AGENTS.md",
        root / "README.md",
        root / "CLAUDE.md",
        root / "ABOUT.md",
    }
    allow_dirs = [root / name for name in ASSET_FOLDERS] + [root / ".audit"]
    for path in root.rglob("*.md"):
        if is_skipped(path):
            continue
        if path in allow_files:
            yield path
            continue
        if any(path.is_relative_to(d) for d in allow_dirs if d.is_dir()):
            yield path


def fix_stale_spaced_refs(root: Path, *, dry_run: bool) -> tuple[int, int]:
    """Replace leftover 'Name with spaces.ext' refs when sanitized file exists."""
    existing: set[str] = set()
    for folder_name in ASSET_FOLDERS:
        folder = root / folder_name
        if not folder.is_dir():
            continue
        for path in folder.rglob("*"):
            if path.is_file() and not is_skipped(path):
                existing.add(path.name)

    # Match filenames with at least one space before a known extension
    spaced_name_re = re.compile(
        r"(?<![\\/\w])([^`\]\n/]*\s[^`\]\n/]*\.(?:pdf|PDF|xlsx|XLSX|jpg|JPG|jpeg|png|md))"
    )

    files_touched = 0
    total_hits = 0

    for md in iter_markdown_for_rewrite(root):
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue
        uniq: dict[str, str] = {}
        for m in spaced_name_re.finditer(text):
            old = m.group(1).strip()
            if "/" in old or "\\" in old or old.startswith("http"):
                continue
            new = sanitize_name(old)
            if new == old or new not in existing:
                continue
            uniq[old] = new
        if not uniq:
            continue
        file_reps = sorted(uniq.items(), key=lambda p: len(p[0]), reverse=True)
        new_text, hits = rewrite_text(text, file_reps)
        if hits == 0:
            continue
        rel = md.relative_to(root).as_posix()
        if dry_run:
            print(f"would rewrite {hits} stale ref(s) in {rel}")
            for old, new in file_reps:
                print(f"  {old} -> {new}")
        else:
            md.write_text(new_text, encoding="utf-8")
            print(f"rewrote {hits} stale ref(s) in {rel}")
        total_hits += hits
        files_touched += 1

    return files_touched, total_hits


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sanitize asset filenames (no spaces) and rewrite MD references"
    )
    parser.add_argument(
        "--root",
        type=Path,
        help="Vault root (default: infer from script location)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print renames/rewrites without writing",
    )
    parser.add_argument(
        "--skip-index",
        action="store_true",
        help="Do not run cleanup_indexes.py (leftover index cleanup) after changes",
    )
    args = parser.parse_args()
    root = args.root.resolve() if args.root else vault_root()

    planned = collect_renames(root)
    conflicts = [(s, d) for s, d, _, _ in planned if d.exists()]
    if conflicts:
        for src, dest in conflicts:
            print(
                f"CONFLICT skip: {src.relative_to(root)} -> "
                f"{dest.relative_to(root)} (exists)"
            )
        planned = [(s, d, o, n) for s, d, o, n in planned if not d.exists()]

    # Apply renames first so replacements match final names on disk
    rename_map: list[tuple[str, str]] = []
    for src, dest, old_name, new_name in planned:
        rename_path(root, src, dest, dry_run=args.dry_run)
        rename_map.append((old_name, new_name))

    # Longest old names first to avoid partial collisions
    rename_map.sort(key=lambda p: len(p[0]), reverse=True)

    total_hits = 0
    files_touched = 0
    for md in iter_markdown_for_rewrite(root):
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue
        new_text, hits = rewrite_text(text, rename_map)
        if hits == 0:
            continue
        rel = md.relative_to(root).as_posix()
        if args.dry_run:
            print(f"would rewrite {hits} ref(s) in {rel}")
        else:
            md.write_text(new_text, encoding="utf-8")
            print(f"rewrote {hits} ref(s) in {rel}")
        total_hits += hits
        files_touched += 1

    stale_files, stale_hits = fix_stale_spaced_refs(root, dry_run=args.dry_run)
    files_touched += stale_files
    total_hits += stale_hits

    print(
        f"Done. renames={len(planned)} files_rewritten={files_touched} "
        f"ref_hits={total_hits}"
    )

    if not args.dry_run and not args.skip_index and (planned or files_touched):
        build = root / ".cursor" / "skills" / "brain-init" / "scripts" / "cleanup_indexes.py"
        if build.is_file():
            subprocess.run(["python3", str(build)], cwd=root, check=False)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
