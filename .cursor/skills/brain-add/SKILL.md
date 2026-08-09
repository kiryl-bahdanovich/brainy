---
name: brain-add
description: >-
  Add or update Markdown notes (and place related files) into the vault's
  personal data folders - calendar, career, documents, finance, health,
  internet, manual, media, sensors, social, statistics, wiki - with YAML
  frontmatter where applicable. Chooses the folder from root and local AGENTS.md
  placement rules.
  Use when creating, editing, drafting, filing, or publishing notes or source
  files in those folders, or when the user asks to add frontmatter to a note.
---

# Brain Add (content folders)

## Scope

Apply to new or updated content under these **personal data** folders only:

| Folder | What goes here (short) |
|--------|------------------------|
| `calendar/` | Schedule exports, events, time blocks |
| `career/` | Work, brand, business artifacts |
| `documents/` | Books, contracts, formal scans/PDFs |
| `finance/` | Income, expenses, statements, money exports |
| `health/` | Labs, meal notes (meal photos/macros → prefer `brain-health`) |
| `internet/` | Saved web articles and excerpts |
| `manual/` | Hand-written notes, journals, self-authored prose |
| `media/` | Photos/audio/video without a stronger domain home |
| `sensors/` | Wearable and personal sensor device exports |
| `social/` | People, relationships, message exports |
| `statistics/` | External reports and datasets (not personal logs) |
| `wiki/` | Formatted docs synthesized from raw sources elsewhere |

**Before every write:** read the target folder's local `AGENTS.md` guide
(e.g. [`manual/AGENTS.md`](../../../manual/AGENTS.md),
[`health/AGENTS.md`](../../../health/AGENTS.md)) for put-here / do-not-put-here /
naming only - do **not** append the new file to that guide. Root placement
reminders live in [`AGENTS.md`](../../../AGENTS.md). Find existing notes with
`brain-search`.

### Do not use this skill for

| Case | Use instead |
|------|-------------|
| Meal / macro logging or health/nutrition *advice* | skill `brain-health` |
| Agent tooling under `.cursor/` | edit skills/docs directly; not brain-add |
| Inventing folders that are not on disk | refuse; place into an existing folder or ask |

Life-event logs go to `.audit/` via skill `brain-audit` - not via brain-add.

## Placement (choose one canonical folder)

1. Prefer the folder the user names, if it matches that folder's `AGENTS.md`.
2. Otherwise pick using root AGENTS quick boundaries:

   - When / schedule → `calendar/`
   - Who / relationship → `social/`
   - Money → `finance/`
   - Career / brand / business artifacts → `career/`
   - Legal / books archive → `documents/`
   - Labs / personal health data / meals → `health/`
   - Wearables / sensor device exports → `sensors/`
   - World reports / datasets → `statistics/`
   - Web clips (not your prose) → `internet/`
   - Your own prose / decisions / journal → `manual/`
   - Orphan media → `media/`
   - Synthesized / formatted pages from raw sources → `wiki/`

3. **One canonical file per fact** - link or short-pointer from elsewhere; do not
   duplicate the same note into two folders.
4. If two folders fit equally, ask once - do not guess.

Default for ambiguous personal writing: `manual/`.

## Frontmatter schema (Markdown)

Every **Markdown** note this skill creates or updates **must** start with YAML
frontmatter in this shape:

```yaml
---
title: Q3 career reflection
description: Notes on career review themes and priorities for next quarter
status: draft
tags:
  - career
  - manual
created: 2026-08-09
source: https://example.com/article   # optional; prefer for internet/
---
```

| Field | Type | Rules |
|-------|------|--------|
| `title` | string | Human-readable title; may differ from filename |
| `description` | string | One sentence summarizing what the note is about |
| `status` | string | One of: `draft`, `active`, `archived` |
| `tags` | string[] | YAML list; see Allowed tags below |
| `created` | date | `YYYY-MM-DD`; set once on create; never overwrite on update |
| `source` | string (optional) | URL or provenance; **include for `internet/`** clips when known |

Non-Markdown binaries (PDF, CSV, ICS, images, zip): place with folder naming
rules only - **no** frontmatter sidecar unless the user asks for a companion `.md`.

## Allowed tags

Use only these values (multiple allowed). Always include the **destination
folder name** as one tag (e.g. note in `career/` → tag `career`).

Folder tags (required one matching the file's folder):

- `calendar`, `career`, `documents`, `finance`, `health`, `internet`,
  `manual`, `media`, `sensors`, `social`, `statistics`, `wiki`

Optional cross-cutting tags:

- `work`, `ai`, `personal`, `business`, `other`

Do not invent tags outside this set.

## Filename conventions

- **No spaces** (skill `brain-fix` Step 2 if a name arrives with spaces).
- Prefer `YYYY-MM-DD-slug.ext` unless the folder's `AGENTS.md` specifies
  another pattern (e.g. `person-firstname-lastname.md` in `social/`,
  `lab-YYYY-MM-DD-slug.pdf` in `health/`).

## Create workflow

1. Confirm feature-branch rules if this creates a **new** tracked file (skill
   `brain-github`: never create new files on `main` / `master`).
2. Choose the destination folder (Placement above); read that folder's `AGENTS.md`.
3. Choose filename per that guide; if a same-path file exists, **update** it
   instead of duplicating.
4. For Markdown: write frontmatter first, then body. Set `created` to today
   (`YYYY-MM-DD`). Defaults when unspecified: `status: draft`, folder tag + any
   other allowed tags that apply.
5. For `internet/`: put the URL in `source` (and/or body) when available.
6. After writing, run post-write cleanup (below).

## Update workflow

1. Read the existing file first.
2. Keep `created` unchanged if present; if missing on a Markdown note, set it
   to today.
3. Preserve unknown/extra frontmatter keys the user already has.
4. Refresh `title`, `description`, `status`, and `tags` only when the edit
   warrants it (or when the user asks). Keep the folder-name tag accurate if
   the file stays in that folder.
5. Ensure Markdown still opens with `---` / frontmatter / `---` before the body.
6. Do not move folders casually; if relocation is needed, follow Placement and
   leave a pointer only when the user wants a redirect.
7. After writing, run post-write cleanup (below).

## Post-write cleanup

After creating or updating a Markdown note, run in order:

1. Read and follow the `brain-fix` skill **Step 1** (typos, grammar, lexis,
   formatting) on **that file** (content-folder Markdown).
2. If the filename has spaces or unsafe characters, run `brain-fix` **Step 2**
   for that path and rewrite references.
3. Do **not** invent `INDEX.md`, `## Index`, or hub notes. Do **not** update
   folder `AGENTS.md` with a file list after add - discovery is `brain-search`
   (hub + frontmatter). A full `brain-init` run is only needed when root/folder
   `AGENTS.md` guides or skills drift from disk - not after every note add.

For binaries: skip Step 1; run Step 2 only if the filename needs sanitizing.

## Body conventions

- Prefer `# Title` as the first body heading only if the body needs structure;
  frontmatter `title` is the canonical title.
- Keep notes in the language the user used unless they ask otherwise.
- Link to related vault paths with normal Markdown links when useful; do not
  build peer-mesh wikilink graphs.

## Checklist

Before finishing:

- [ ] Target folder exists on disk and matches its local `AGENTS.md`
- [ ] File is under one of the personal data folders (not an invented path)
- [ ] Specialized cases deferred (`brain-health` meal log, etc.) when required
- [ ] Markdown has valid YAML frontmatter with all required fields
- [ ] `created` is `YYYY-MM-DD` and not clobbered on update
- [ ] `tags` includes the folder name and only allowed values
- [ ] Filename has no spaces; dated slug preferred where the folder guide says so
- [ ] One canonical location; no duplicate fact in a second folder
- [ ] Ran `brain-fix` Step 1 on written Markdown (and Step 2 if names needed it)
- [ ] Did not add an index entry or file list to any `AGENTS.md`
- [ ] New files were not created on `main` / `master` (`brain-github`)
