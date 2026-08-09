---
name: brain-search
description: >-
  Find notes in personal data folders by hub (folder) scope plus YAML
  frontmatter (title, description, status, tags, created, source) and filename
  - without reading note bodies to decide relevance. Use when searching,
  finding, listing, or filtering vault notes by topic, tag, status, folder, or
  keywords, and when answering questions about the user or vault knowledge
  (then read matched bodies and follow links only after frontmatter match).
  Starts from content-folder hubs, then frontmatter search only.
---

# Brain search (hub-first, frontmatter-only match)

## Rule

**Never read a note body to decide relevance.** Match on **hub (folder) scope**
plus **frontmatter** (and filename) only. Only after a note matches, `Read` its
body for content, quotes, or link-following.

## Scope

Personal data folders (each folder is a **hub**):

| Hub / folder | Role |
|--------------|------|
| `calendar/` | Schedule, events, time blocks |
| `career/` | Work, brand, business |
| `documents/` | Books, contracts, formal docs |
| `finance/` | Money trails |
| `health/` | Labs, nutrition |
| `internet/` | Web clips and excerpts |
| `manual/` | Self-authored notes and journals |
| `media/` | Orphan photos/audio/video |
| `sensors/` | Wearable and personal sensor data |
| `social/` | People and relationships |
| `statistics/` | External reports and datasets |
| `wiki/` | Formatted docs synthesized from raw sources |

Search only `*.md` that have YAML frontmatter. Skip `AGENTS.md` (hub **guides**,
not inventories), root agent docs, and files without a frontmatter block.

This skill **is** vault discovery. Do **not** invent or read `INDEX.md` /
`## Index` inventories. Do **not** Grep whole-file bodies as the primary
filter. Nobody maintains a file list in `AGENTS.md`.

## Hubs (use first)

1. **Pick hub(s)** from the query using root [`AGENTS.md`](../../../AGENTS.md)
   placement boundaries (when → calendar, who → social, money → finance, career
   / brand → career, legal/books → documents, labs/meals → health, wearables →
   sensors, world data → statistics, web clips → internet, own prose → manual,
   orphan media → media, synthesized pages → wiki). Folder `AGENTS.md` guides
   define boundaries only - not note lists.
2. **Search frontmatter inside those hubs first** (script `--hub` / `--folder`).
3. If the hub scope is empty or clearly too narrow, expand to **all** content
   hubs once (omit `--hub`).
4. If a hub folder is missing on disk, say so; do not invent paths. Suggest
   skill `brain-init` only when layout docs look stale.

Hub choice is a **navigation aid**. Accepted matches still need verified
frontmatter before you treat them as hits.

## Frontmatter fields used for matching

| Field | Role |
|-------|------|
| `title` | Primary topical match |
| `description` | One-line summary match |
| `tags` | Folder tags + cross-cutting (`work`, `ai`, …) per `brain-add` |
| `status` | `draft`, `active`, `archived` |
| `created` | Date filter / chronology |
| `source` | URL / provenance (especially `internet/`) |
| filename | `YYYY-MM-DD-slug.md` (and folder path) also searchable |

Body text is **out of scope for matching**.

## Workflow

1. Map the query to one or more hubs (folders).
2. Run the frontmatter search script with `--hub` when scoped; omit `--hub` only
   when the query is cross-cutting or the hub miss is clear.
3. Prefer the script (or Grep limited to frontmatter keys:
   `^title:`, `^description:`, `^tags:`, `^  - `, `^status:`, `^created:`,
   `^source:`). Do **not** full-body Grep to find candidates.
4. Present matching notes with path + frontmatter summary.
5. **Only then** `Read` matched files if the user needs body content or an
   answer grounded in the note.
6. **After match only:** when answering substantive questions, follow Markdown /
   wikilinks from accepted notes - but frontmatter-check each new candidate
   before treating it as in-scope. Do not walk the whole vault via bodies.
7. If zero matches in hub scope, widen to all hubs once; if still empty, say so.
   Do not fall back to full-body vault scans unless the user asks.

## Script

From the vault root:

```bash
python3 .cursor/skills/brain-search/scripts/search_frontmatter.py QUERY...
python3 .cursor/skills/brain-search/scripts/search_frontmatter.py --hub career review
python3 .cursor/skills/brain-search/scripts/search_frontmatter.py --tag ai --status draft
python3 .cursor/skills/brain-search/scripts/search_frontmatter.py Kubernetes --hub internet --json
```

| Flag | Meaning |
|------|---------|
| `QUERY...` | All terms must appear in title/description/tags/status/created/source/filename |
| `--hub NAME` | Limit to that content folder (repeatable). Same as `--folder` |
| `--tag TAG` | Require tag (repeatable) |
| `--status draft\|active\|archived` | Filter by status |
| `--folder NAME` | Limit folder (repeatable; default: all content hubs) |
| `--json` | Machine-readable list for follow-up Reads |

The script reads each file only enough to parse the opening YAML block; it does
**not** use the markdown body for matching.

## Manual fallback (no script)

1. Pick hub folder(s); else Glob `*/*.md` under the content folders.
2. Skip `AGENTS.md` and files without opening `---`.
3. For each candidate, read **only the frontmatter** (stop after the closing
   `---`), or Grep frontmatter-key patterns only.
4. Rank/filter by the query.
5. Read full files only for accepted matches.

## Response shape

Keep results short:

- Path
- `title` / `description`
- `status`, `tags`, `created` (and `source` when present)

Open bodies only when answering from note content or when the user asks to open
them.
