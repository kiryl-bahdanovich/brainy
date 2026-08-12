---
name: brain-audit
description: >-
  Log categorized life/work/business events as Markdown notes under .audit/
  (one file per event) with YAML frontmatter including life categories; batch
  log several events; or analyze the journal by category, date range, mood, or
  people. Use when the user asks to audit, log, record an event, life journal,
  analyze audit, or names brain-audit.
---

# Brain Audit (life event journal)

## Scope

Only apply to Markdown files under:

- `.audit/` - chronological event journal (decisions, milestones, health, money,
  career, mood, meetings, and similar dated facts). Agent tooling, not a
  personal-data content folder.

Do **not** auto-log every chat or agent session. Write only when the user asks
to record an event (or names this skill). Do **not** place audit notes under
content folders (`manual/`, `career/`, etc.) or invent `## Related` /
`## Index` inventories. Discover past events by scanning `.audit/`
frontmatter (analyze mode) - not via an index file.

## Modes

| Mode | When | Action |
|------|------|--------|
| **log** (default) | One event to record | Create or update one note |
| **batch** | Several events in one message | One file per event; then one post-write cleanup pass |
| **analyze** | User asks for journal review / life analysis | Scan frontmatter of `.audit/*.md` first, open bodies only for matches; summarize by category, date range, mood, people. Never invent events. |

## Frontmatter schema

Every note **must** start with YAML frontmatter:

```yaml
---
title: Signed apartment lease
description: Signed lease renewal for another year
status: active
tags:
  - apartment
  - lease
categories:
  - home
  - money
mood: 4
people: []
created: 2026-07-31
---
```

| Field | Type | Required | Rules |
|-------|------|----------|--------|
| `title` | string | yes | Human-readable title; may differ from filename |
| `description` | string | yes | One sentence summarizing the event |
| `status` | string | yes | One of: `draft`, `active`, `archived` |
| `tags` | string[] | yes | Auto-generated from event context; see Tags below |
| `categories` | string[] | yes | Life domains for analysis; only allowed categories below; at least one |
| `mood` | int | no | `1`-`5` when the event has an emotional signal; omit if unknown |
| `people` | string[] | no | Short names when relevant; omit or `[]` if none |
| `created` | date | yes | `YYYY-MM-DD`; set once on create; never overwrite on update |

## Tags

`tags` are **not** a fixed allowlist. Generate them from the event and vault
context (at least one required). Prefer short lowercase slug-style labels
(`kebab-case` or single words).

How to choose:

1. Use any tags the user names explicitly.
2. Otherwise infer from what happened: domain signals, themes, outcomes,
   places, tools, projects, or recurring motifs in the note.
3. Prefer reusing tags already present on other `.audit/*.md` notes when they
   fit (scan frontmatter before inventing a near-duplicate synonym).
4. Do not dump categories into `tags` by default - categories are the life-
   domain axis; tags are freeform filters for search/analyze.
5. Prefer 1–4 precise tags over a long laundry list; skip vague fillers like
   `other` or `misc` unless nothing else fits.

Example: lease renewal → `tags: [apartment, lease]` with
`categories: [home, money]`.

## Allowed categories

Life domains for analysis (multiple allowed; at least one required):

- `health`
- `money`
- `career`
- `business`
- `ai`
- `relationships`
- `mood`
- `decision`
- `learning`
- `travel`
- `home`
- `other`

### Category mapping hints

Infer when the user omits categories; ask only if ambiguous.

| Signal | Categories |
|--------|------------|
| Doctor, labs, supplements, symptoms, workout, meal macros | `health` |
| Salary, rent, invest, spend, net worth | `money` |
| Job, employer, promotion, performance | `career` |
| Clients, consulting, side project revenue | `business` |
| Models, agents, AI study/product | `ai` |
| Partner, family, friends, date | `relationships` (+ `mood` if emotional) |
| Explicit mood / energy / "feeling" | `mood` |
| Chose X over Y, committed to a plan | `decision` |
| Course, book, deliberate practice | `learning` |
| Trip, flight, hotel | `travel` |
| Lease, apartment, furniture, chores | `home` |
| Unclear residual | `other` |

Tags are independent of categories: e.g. salary raise →
`tags: [salary, raise]` + `categories: [money, career]`.

## Filename convention

`YYYY-MM-DD - Short Title.md` under `.audit/`.

- Date = **event date** (default today if the user omits it)
- Spaces are allowed in audit filenames
- If a same date + title file already exists, **update** it instead of creating a duplicate

## Create workflow (log / batch)

1. Parse the event: what happened, when, optional context/outcome, mood /
   people if given (if the input is a charged narrative rather than clean
   facts, run `brain-clarity` first and use its Facts bucket here, mood from
   its Emotions bucket); generate `tags` from context (and existing `.audit/`
   vocabulary); set `categories` from the allowed list (ask if ambiguous).
2. Ensure `.audit/` exists (create it if missing; keep `.audit/.gitkeep` if present).
3. Choose filename: `YYYY-MM-DD - Short Title.md`.
4. Write frontmatter first, then body (template below).
5. Set `created` to the event date (`YYYY-MM-DD`). Defaults when unspecified:
   `status: active`, at least one context-generated tag, at least one allowed
   category.
6. Prefer short factual notes over essays.
7. After writing all files in this turn, run post-write cleanup (below).

## Update workflow

1. Read the existing file first.
2. Keep `created` unchanged if present; if missing, set it to the event date (or today).
3. Preserve unknown/extra frontmatter keys the user already has.
4. Refresh `title`, `description`, `status`, `tags`, and `categories` only when
   the edit warrants it; add `mood` / `people` when newly known.
5. Ensure the file still opens with `---` / frontmatter / `---` before the body.
6. After writing, run post-write cleanup (below).

## Analyze workflow

1. Scan frontmatter of `.audit/*.md` first (do not invent an index file).
2. Filter by user criteria: category, tag, date range, mood, people, keywords.
3. Open note bodies only for matching files.
4. Summarize themes, patterns, decisions, and open outcomes - cite filenames.
5. Do **not** invent events or fill gaps with speculation.

## Body template

```markdown
## What happened

...

## Context

... (omit section if empty)

## Outcome / next

... (omit section if empty)

## Links

... (omit section if empty; health/food or content-folder paths useful for later analysis)
```

Prefer `# Title` only if the body needs structure; frontmatter `title` is canonical.

## Post-write cleanup

After creating or updating note(s) under `.audit/`, run once per turn after batch:

1. Apply `brain-fix` Step 1 (typos, grammar, lexical, formatting) to each
   written file.
2. Do **not** create `INDEX.md` / `## Index` under `.audit/` or the vault root,
   and do **not** append audit entries to any `AGENTS.md`.

## Checklist

Before finishing (log / batch):

- [ ] File(s) under `.audit/`
- [ ] Filename is `YYYY-MM-DD - Short Title.md`
- [ ] Valid YAML frontmatter with all required fields
- [ ] `categories` is a non-empty YAML list using only allowed life categories
- [ ] `tags` is a non-empty YAML list auto-generated from event/vault context
  (reuse existing audit tags when they fit; no fixed allowlist)
- [ ] `mood` / `people` present only when known
- [ ] `created` is `YYYY-MM-DD` and not clobbered on update
- [ ] Body starts after the closing `---`
- [ ] Ran `brain-fix` Step 1 on each written file

Before finishing (analyze):

- [ ] Used `.audit/` frontmatter before bodies
- [ ] Summary grounded only in existing notes
- [ ] Cited filenames for key claims
