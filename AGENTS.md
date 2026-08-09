# Brainy

Personal knowledge vault. Prefer skills under `.cursor/skills/` for detailed workflows.

**Personal configuration:** fill in [`ABOUT.md`](./ABOUT.md) when setting up your
own Brain (who you are, priorities, health/diet/timezone, work preferences).
Skills read it for context. Keep real personal details in a private copy.

## Layout

Top-level folders are **personal data sources** (hubs). Each has a local
`AGENTS.md` hub **guide**: purpose, put-here / do-not-put-here, naming, and
skills - **not** a file inventory. Do **not** maintain `INDEX.md`, `index.md`,
`## Index`, or `*-INDEX.md`. Find notes with skill `brain-search` (hub + YAML
frontmatter only).

| Folder | Role | Local guide |
|--------|------|-------------|
| [`calendar/`](./calendar/) | Schedule exports, events, time blocks | [`AGENTS.md`](./calendar/AGENTS.md) |
| [`career/`](./career/) | Work, brand, business (reviews, offers, drafts, consulting) | [`AGENTS.md`](./career/AGENTS.md) |
| [`documents/`](./documents/) | Books, contracts, formal scans/PDFs | [`AGENTS.md`](./documents/AGENTS.md) |
| [`finance/`](./finance/) | Income, expenses, statements, money exports | [`AGENTS.md`](./finance/AGENTS.md) |
| [`health/`](./health/) | Medical records, nutrition, wearables | [`AGENTS.md`](./health/AGENTS.md) |
| [`internet/`](./internet/) | Saved web articles and excerpts | [`AGENTS.md`](./internet/AGENTS.md) |
| [`manual/`](./manual/) | Hand-written notes and journals | [`AGENTS.md`](./manual/AGENTS.md) |
| [`media/`](./media/) | Photos, audio, and other media without a stronger domain | [`AGENTS.md`](./media/AGENTS.md) |
| [`social/`](./social/) | People, relationships, messages | [`AGENTS.md`](./social/AGENTS.md) |
| [`statistics/`](./statistics/) | External reports and datasets (not personal logs) | [`AGENTS.md`](./statistics/AGENTS.md) |

Agent tooling (not personal sources): [`.cursor/skills/`](./.cursor/skills/), [`.audit/`](./.audit/) (life-event journal via `brain-audit`). Root [`CLAUDE.md`](./CLAUDE.md) points here as the source of truth.

| Skill | Role |
|-------|------|
| [`brain-add`](./.cursor/skills/brain-add/SKILL.md) | Add/update notes in content folders with YAML frontmatter |
| [`brain-audit`](./.cursor/skills/brain-audit/SKILL.md) | Log dated life/work events under `.audit/` |
| [`brain-critical`](./.cursor/skills/brain-critical/SKILL.md) | Stress-test claims; calibrate confidence |
| [`brain-fix`](./.cursor/skills/brain-fix/SKILL.md) | Proofread notes; sanitize asset filenames |
| [`brain-github`](./.cursor/skills/brain-github/SKILL.md) | Feature branch, PR, and merge workflow |
| [`brain-goal`](./.cursor/skills/brain-goal/SKILL.md) | Multi-approach problem solving via hubs + vault notes |
| [`brain-health`](./.cursor/skills/brain-health/SKILL.md) | Health advice + per-meal notes under health/ |
| [`brain-init`](./.cursor/skills/brain-init/SKILL.md) | Sync AGENTS.md / skills with on-disk layout |
| [`brain-search`](./.cursor/skills/brain-search/SKILL.md) | Find notes via folder hubs + frontmatter only |
| [`brain-soul`](./.cursor/skills/brain-soul/SKILL.md) | Companion opinion grounded in ABOUT.md |

Empty folders keep a `.gitkeep` so git tracks them.

## Placement rules

1. Read the target folder's `AGENTS.md` guide before adding files (boundaries only - do not append file lists to it).
2. One canonical file per fact - link from other places, do not duplicate.
3. Filenames: no spaces (skill `brain-fix` Step 2); prefer `YYYY-MM-DD-slug.ext`.
4. Discover existing notes via `brain-search` - never by maintaining an index.

Quick boundary reminders:

- When / schedule → `calendar/` · Who / relationship → `social/` · Money → `finance/`
- Career / brand / business artifacts → `career/` · Legal/books archive → `documents/`
- Labs / meal notes / Strava → `health/` · World reports/datasets → `statistics/`
- Web clips → `internet/` · Your own prose → `manual/` · Orphan media → `media/`

## Processing

- "process" without a named step → typo/grammar/lexis/formatting where the skill applies (`brain-fix` Step 1)
- Filename / no-spaces cleanup on content folders → `brain-fix` Step 2
- Structure sync → skill `brain-init` (align root and folder `AGENTS.md` / skills with disk)
- Do not reorganize meaning unless asked

## Git / PRs

- Skill: [`brain-github`](.cursor/skills/brain-github/SKILL.md)
- **New files:** feature branch only - never create on `main` / `master`
- **Save:** commit all changes, push, open a PR (**not draft**), return the URL, then always ask whether to merge into `main`
- **Merge:** only after explicit yes - `gh pr merge <n> --squash --delete-branch`, confirm branch deleted

## Agent docs sync

- Keep each content folder's `AGENTS.md` guide in sync when that folder's **role** changes (purpose / boundaries / naming) - not as a file list
- Do not invent folders that are not on disk
- Skill `brain-init` removes leftover index files; it must not write inventories into `AGENTS.md`
