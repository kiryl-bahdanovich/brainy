---
name: brain-fix
description: >-
  Process Markdown notes under content folders and .audit/ (typos, grammar,
  lexis, formatting) and sanitize asset filenames without spaces, rewriting all
  markdown references. Use when the user asks to process, clean, polish,
  proofread notes, or fix filenames with spaces / broken asset links.
---

# Brain Fix

## Scope

1. **Markdown under content folders and `.audit/`** - typos, grammar, lexis,
   formatting (Step 1).
2. **Content folders** (`calendar/`, `career/`, `documents/`, `finance/`,
   `health/`, `internet/`, `manual/`, `media/`, `sensors/`, `social/`,
   `statistics/`, `wiki/`) - filename sanitization without spaces **and** rewrite
   of all markdown references to those files (Step 2).

**Do not** apply Step 2 to `.audit/` event notes: that journal allows spaces in
`YYYY-MM-DD - Short Title.md` (skill `brain-audit`).

For frontmatter create/update rules, follow the `brain-add` skill (or
`brain-audit` for `.audit/`). This skill does not invent or rewrite frontmatter
unless the user asks.

## Pipeline

Run steps in order. Only perform steps the user requested; if they say
"process" without naming a step, run **Step 1** only. If they ask to fix
filenames / spaces in names / link-safe names / broken asset links, run
**Step 2** (and Step 1 only if they also asked to process prose).

### Step 1 - Typos, grammar, lexis, formatting

1. Read the target note(s). If unspecified, ask which file(s) - do not batch a
   whole content folder or `.audit/` unless asked.
2. Fix **spelling**, **grammar**, and **punctuation** without changing meaning,
   tone, or structure of ideas.
3. Fix **lexical** errors without changing meaning, tone, or structure of ideas:
   - Wrong word choice
   - Calques / unnatural phrasing
   - Clearly awkward wording that a fluent reader would fix
4. Fix **Markdown formatting** only:
   - Consistent heading levels (`#` / `##` / `###`)
   - Lists: consistent `-` or `1.` markers; fix broken indentation
   - Blank lines around headings, lists, and code fences
   - Broken or incomplete code fences
   - Obvious spacing issues (double spaces, trailing spaces)
5. Do **not**:
   - Expand, summarize, or reorganize content
   - Rewrite for style or "polish" beyond clear errors
   - Change filenames (use Step 2 for content-folder files)
   - Alter YAML frontmatter keys/values (except fixing typos inside string
     values if clearly erroneous)
   - Convert wikilinks `[[...]]` or tags unless broken
6. Write the corrected file in place.
7. Briefly summarize what changed (categories: typos / grammar / lexis /
   formatting).

### Step 2 - Filenames without spaces + fix links

Goal: every **content-folder** filename has **no spaces**, and every markdown
reference to those files points at the **new** name (links, backticks, path
strings).

Prefer the script (rename + rewrite + remove leftover indexes in one pass):

```bash
python3 .cursor/skills/brain-fix/scripts/sanitize_asset_filenames.py
# preview:
python3 .cursor/skills/brain-fix/scripts/sanitize_asset_filenames.py --dry-run
```

Manual equivalent if the script cannot run:

1. Target folders (unless the user names specific paths): `calendar/`,
   `career/`, `documents/`, `finance/`, `health/`, `internet/`, `manual/`,
   `media/`, `sensors/`, `social/`, `statistics/`, `wiki/`. Skip `.audit/`.
2. For each file whose **name** contains a space:
   - Replace each run of whitespace with a single `-`
   - Collapse repeated `-` to one `-`
   - Trim leading/trailing `-` from the stem (keep the extension)
   - Example: `Scan june 2025.pdf` → `Scan-june-2025.pdf`
   - Do not create vault `index.md` / `INDEX.md`, hub-prefixed `*-INDEX.md`,
     or `## Index` inventories; do not append file lists to `AGENTS.md`
3. If the target name already exists, do not overwrite - report the conflict and
   skip.
4. `git mv` when the path is tracked; otherwise filesystem rename.
5. **Rewrite references** in content markdown only: content folders, `.audit/`
   note bodies, and root `AGENTS.md` / `README.md` / `CLAUDE.md` / `ABOUT.md`.
   Do **not** rewrite `.cursor/plans/`, skill example text, or
   `cleanup_indexes.py` inventory-name patterns. For each `old_name` → `new_name`,
   replace occurrences in:
   - Markdown links: `[label](.../old_name)` / `[label](./old_name)`
   - Backticks: `` `old_name` ``
   - Plain path / filename mentions
6. Remove leftover index inventories (do not create new ones):
   `python3 .cursor/skills/brain-init/scripts/cleanup_indexes.py`
7. Summarize: old → new for each rename; files where refs were rewritten; skips.

## Later steps (not implemented yet)

Reserve for future skill updates, e.g. structure.
Do not invent extra steps beyond Step 1 / Step 2 unless this skill is extended.

## Checklist (Step 1)

- [ ] File is under a content folder or `.audit/`
- [ ] Meaning and intent unchanged
- [ ] Typos / grammar / punctuation fixed
- [ ] Lexical errors fixed (word choice, calques, awkward wording)
- [ ] Markdown formatting cleaned without restructuring ideas
- [ ] Frontmatter left intact (unless user asked otherwise)

## Checklist (Step 2)

- [ ] Only content-folder paths (or user-named files); skipped `.audit/`
- [ ] No spaces left in renamed content-folder filenames
- [ ] No overwrite conflicts
- [ ] Markdown links / backticks / path mentions updated to new names
- [ ] Leftover indexes removed via `cleanup_indexes.py` (not regenerated)
- [ ] Did not rewrite plans / skill examples / inventory-name patterns
