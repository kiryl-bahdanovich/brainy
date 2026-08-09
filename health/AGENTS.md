# health/

## Purpose

Body and health sources: clinical records and nutrition.

## Put here

- Labs, imaging, clinical PDFs and reports
- One Markdown note per meal/drink when logging food (skill `brain-health` log mode)

## Do not put here

- Wearable / sensor device exports → [`../sensors/`](../sensors/)
- Generic photos with no health meaning → [`../media/`](../media/)
- Public health statistics about the world → [`../statistics/`](../statistics/)
- Diet opinions without personal data → [`../manual/`](../manual/) or [`../internet/`](../internet/)
- A single aggregate food table (`Food.md` is retired - do not create it)
- File inventories or index lists (this guide is not an index)

## Naming (important - flat folder)

- Labs: `lab-YYYY-MM-DD-slug.pdf`
- Meals: `YYYY-MM-DD-meal-slug.md` / `YYYY-MM-DD-drink-slug.md` (frontmatter required)
- Do not archive meal photos unless the user asks

## Skills

- `brain-health` - safe health advice and per-meal notes under this folder
- Find past meals via skill `brain-search` (hub `health` + frontmatter)
- Wearable raw data lives in [`../sensors/`](../sensors/); search hub `sensors` when needed

## Shared rules

- Filenames: no spaces (skill `brain-fix` Step 2); prefer `YYYY-MM-DD-slug.ext`
- One canonical file per fact; other folders get a link or short pointer, not a duplicate
- This file is a hub **guide** (structure and purpose only) - not a file index
- Find notes via skill `brain-search` (hub + frontmatter); do not add `## Index` or file lists here
- Parent vault docs: [`../AGENTS.md`](../AGENTS.md), [`../ABOUT.md`](../ABOUT.md)
