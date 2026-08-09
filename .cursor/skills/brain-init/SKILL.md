---
name: brain-init
description: >-
  Sync AGENTS.md, CLAUDE.md, folder AGENTS.md files, and .cursor/skills/ to the
  vault's on-disk layout; remove leftover INDEX.md / index.md inventories; fix
  broken wikilinks in content folders when present. Use when the user asks to
  init, sync, refresh, or realign agent docs/skills with the vault structure,
  after renaming/moving content folders or skills, or when layout docs look stale.
---

# Brain Init (structure sync)

Reconcile agent **structure guides** and skills with the **on-disk** vault
layout. Do not invent folders or skills that do not exist. Remove leftover
index inventories (do not write new ones, and do **not** write file lists into
`AGENTS.md`).

## When to run

- User says init / sync / refresh agent docs / update skills to match structure
- After rename/move of content folders or skill directories
- When AGENTS.md Layout or skill paths look stale
- After adding/removing content folders (keep layout docs current)
- When wikilinks in content notes look broken

Do **not** invent `INDEX.md`, `## Index`, or Related meshes. Each folder
`AGENTS.md` is a **hub guide** (purpose / boundaries / naming only). Discovery
is skill `brain-search` (hub + frontmatter) - nobody maintains an index list.

## Inventory (do this first)

From the vault root, discover reality with shell/`Glob` (ignore `.git`,
`.obsidian`, `.trash`, `.DS_Store`):

1. **Top-level content folders** when present: `calendar/`, `career/`,
   `documents/`, `finance/`, `health/`, `internet/`, `manual/`, `media/`,
   `social/`, `statistics/`. Each should have a local `AGENTS.md`. Do **not**
   create `index.md` or root `INDEX.md`.
2. **Agent tooling**: `.cursor/skills/`, `.audit/` (life-event journal; not a
   content folder).
3. **Skills**: every directory under `.cursor/skills/*/SKILL.md`. Record `name`
   from frontmatter and one-line purpose from `description`.
4. **Scripts**: any `scripts/` under those skills (paths must stay correct).
5. **Root agent files**: `AGENTS.md`, `CLAUDE.md` (must exist after this skill
   runs). Root `INDEX.md` and per-folder `index.md` must **not** exist.

Do not treat `.cursor/`, `.obsidian/`, `.trash`, `.git/`, or `.audit/` as
personal-data content folders in the Layout table (`.audit/` is tooling).

## What to update

### 1. Remove index inventories (required)

```bash
python3 .cursor/skills/brain-init/scripts/cleanup_indexes.py
```

The script **only deletes** leftover root `INDEX.md` / `index.md`, every
content-folder `index.md`, and leftover `*-INDEX.md` inventories. It does
**not** write new index files and must **not** append inventories into
`AGENTS.md`. Optional: `--stdout` prints a navigation report without writing.

### 2. Wikilinks (optional, when content notes use `[[...]]`)

```bash
python3 .cursor/skills/brain-init/scripts/fix_links.py
# preview:
python3 .cursor/skills/brain-init/scripts/fix_links.py --dry-run
```

| Action | Rule |
|--------|------|
| **Fix broken links** | If `[[Target]]` uniquely matches a note stem/title after normalization, rewrite to the real stem. Preserve `\|alias` when present. |
| **Leave unresolved** | Missing notes with no unique match - report only; do not create notes. |
| **Skip ambiguous** | Multiple matches - report; do not guess. |

Do **not** invent `## Related` hub meshes or category overview notes.

### 3. `AGENTS.md`

Keep personal/priority sections unless the user asks to change them.

Update structure-dependent sections so they match inventory:

- **Layout** - real content folders + agent tooling (`.cursor/skills/`, `.audit/`)
  with **current** skill names
- **Placement / Processing** - skills and folders that actually exist
- Cross-references to skills must use **actual** skill directory/`name` values
- Keep the rule that folder `AGENTS.md` files are guides, not inventories

### 4. `CLAUDE.md`

Keep as a thin pointer to `AGENTS.md` unless the user asks otherwise:

```markdown
# Project instructions

See [AGENTS.md](./AGENTS.md). Follow that file as the source of truth.
```

### 5. Each content folder `AGENTS.md`

Update **purpose / put-here / do-not-put-here / naming / skills** so they match
how the folder is actually used. Do not invent subfolders. Do **not** add
`## Index`, file lists, or inventories - discovery stays with `brain-search`.

### 6. Every skill under `.cursor/skills/`

| Check | Action |
|-------|--------|
| Scope folders | Match on-disk content hubs only (no stale folder names) |
| Sibling skill references | Rename to current skill `name`s |
| Script paths in docs | Match real path under `.cursor/skills/<skill>/…` |
| Descriptions | Still accurate for WHAT/WHEN after path fixes |

**Preserve** intentional conventions unless structure forces a change
(frontmatter schemas, allowed tags, pipeline steps).

Do **not** delete skills or notes unless the user explicitly asks.

### 7. Stale / duplicate skills

If inventory shows renamed leftovers (old folder still present beside the new
one), report them and ask before deleting. Prefer updating references over
silent removal.

## Workflow checklist

```
Brain-init progress:
- [ ] Inventory folders + skills + scripts + .audit
- [ ] Diff inventory vs AGENTS.md / CLAUDE.md / folder AGENTS.md / skills
- [ ] Remove leftover indexes via cleanup_indexes.py
- [ ] Fix broken wikilinks via fix_links.py (if any content notes use them)
- [ ] Patch AGENTS.md + folder AGENTS.md + skills for path/name drift
- [ ] Ensure CLAUDE.md → AGENTS.md
- [ ] If ABOUT.md is still TBD, remind once to fill personal configuration
- [ ] Summarize changes + unresolved links + leftovers needing a decision
```

## Response shape

Be short:

1. What the vault actually contains (folders + skill names)
2. What was updated (files touched)
3. Unresolved links / anything needing a user decision

## Constraints

- Source of truth = filesystem, not outdated prose in AGENTS.md
- Do not rewrite ABOUT.md biography/priorities unless asked
- If ABOUT.md is still all `TBD` after setup, remind the user once to fill it
  (personal configuration) - do not invent biography
- Do not create empty note folders “for completeness”
- Do not create missing notes just to satisfy a wikilink
- Prefer surgical edits; keep skill bodies concise
- Always run `cleanup_indexes.py` (cleanup only) on every brain-init run
- Never invent `INDEX.md`, `## Index`, Related hub graphs, or file lists inside `AGENTS.md`
