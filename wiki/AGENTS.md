# wiki/

## Purpose

Formatted, synthesized documents built from raw sources elsewhere in the vault
(media, manual, health, sensors, internet, etc.). The durable “finished page”
layer - not the landing zone for raw exports or scratch notes.

## Put here

- Polished topic pages, summaries, and structured write-ups derived from other hubs
- Cross-source syntheses (e.g. a health overview that cites labs + sensor exports)
- Long-lived reference articles you want to maintain as the canonical explanation
- Pages that link back to raw sources rather than duplicating them

## Do not put here

- Raw media, photos, audio → [`../media/`](../media/)
- Scratch journals, diaries, working prose → [`../manual/`](../manual/)
- Labs, meal logs, clinical PDFs → [`../health/`](../health/)
- Wearable / sensor dumps → [`../sensors/`](../sensors/)
- Web clips as-saved → [`../internet/`](../internet/)
- Formal legal/books/scans archive → [`../documents/`](../documents/)
- File inventories or index lists (this guide is not an index)

## Naming

- Prefer stable topic slugs: `topic-slug.md` (e.g. `sleep-baseline.md`)
- Or dated when the page is a snapshot: `YYYY-MM-DD-topic-slug.md`
- No spaces in filenames
- Link to source notes with Markdown paths; do not copy raw files into this folder

## Skills

- Create / update wiki pages via skill `brain-add` (hub `wiki`)
- Find wiki pages via skill `brain-search` (hub `wiki` + frontmatter)

## Shared rules

- Filenames: no spaces (skill `brain-fix` Step 2); prefer `YYYY-MM-DD-slug.ext`
- One canonical file per fact; other folders get a link or short pointer, not a duplicate
- This file is a hub **guide** (structure and purpose only) - not a file index
- Find notes via skill `brain-search` (hub + frontmatter); do not add `## Index` or file lists here
- Parent vault docs: [`../AGENTS.md`](../AGENTS.md), [`../ABOUT.md`](../ABOUT.md)
