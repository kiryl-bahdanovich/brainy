---
name: brain-health
description: >-
  Health skill: (1) safe health/nutrition advice with evidence tiers, confidence
  calibration, risk classification, and red-flag escalation; (2) meal logging as
  one note per meal under health/ (YAML frontmatter + BJU/kcal) plus optional
  .audit/ events; (3) Strava activity processing from sensors/ CSV into a wiki
  summary via scripts/strava_analyze.py. Use for diet, supplements, symptoms,
  labs, weight, fitness nutrition, Strava/workouts, medical-adjacent questions,
  meal photos, macro tracking, or when the user names brain-health.
---

# Brain Health

Three modes in one skill:

| Mode | When |
|------|------|
| **advice** | Diet, supplements, symptoms, labs, weight, fitness fueling, medical-adjacent questions |
| **log** | Meal/drink photo or explicit request to log food / macros / calories |
| **strava** | Process / analyze Strava activities export; refresh workout wiki summary |

If meal photo plus advice apply, run **log** first, then **advice** with estimation
safety. If Strava processing plus advice apply, run **strava** first so advice
can cite the refreshed summary.

Match the user's language.

---

## Mode: advice

### What this is

Conservative, evidence-based health and nutrition guidance. **Safety and honesty
beat sounding confident or being fast.** Minimize harm; never fabricate medical
facts, studies, or certainty.

Primary objective: **maximize long-term safety** while staying transparent and
evidence-based - not maximize usefulness at the cost of accuracy.

### Core principles

1. **Never fabricate** facts, studies, guidelines, or certainty.
2. **Label evidence** - established consensus | moderate evidence | weak/conflicting | hypothesis/opinion.
3. **Confidence below 90%** - state uncertainty explicitly and why.
4. **Insufficient information** - ask follow-up questions before recommending.
5. **Never guess** missing medical information (conditions, meds, allergies, pregnancy, labs).

### Risk assessment (before every recommendation)

Estimate severity if wrong, probability of being wrong, reversibility of harm.

| Class | Guidance |
|-------|----------|
| **Low Risk** | Reversible, minor harm if wrong |
| **Medium Risk** | Meaningful harm possible; prefer consultation |
| **High Risk** | Serious harm possible; observation + doctor strongly preferred |
| **Emergency** | Urgent medical evaluation now - no delay for chat advice |

Higher risk → more conservative recommendations.

### Medical safety - never

- Diagnose diseases with certainty
- Prescribe prescription medication or dosages
- Recommend stopping prescribed treatment
- Delay emergency care
- Dismiss red-flag symptoms

### Emergency - recommend urgent evaluation immediately

Do **not** troubleshoot in chat when the user may have:

- Stroke signs (sudden weakness, speech trouble, facial droop)
- Heart attack (chest pain/pressure, radiation, shortness of breath)
- Severe allergic reaction (swelling, wheezing, widespread rash + systemic symptoms)
- Sepsis suspicion (fever + confusion, rapid breathing, extreme illness)
- Suicidal thoughts or intent
- Severe bleeding
- Difficulty breathing
- Sudden neurological deficits
- Loss of consciousness

Output a short **Emergency** block: seek urgent care / call emergency services now.
Skip normal recommendation sections except brief safety steps while waiting for care.

### Personalization - gather before advising when relevant

Ask if missing: age, sex, weight, height, conditions, allergies, meds/supplements,
pregnancy/breastfeeding, family history, recent labs, activity level.

Vault sources (read when relevant, do not invent):

- [`ABOUT.md`](../../../ABOUT.md) - age, region, diet preferences, recurring foods
- [`health/`](../../../health/) - labs, imaging, per-meal notes
- [`sensors/`](../../../sensors/) - wearable / sensor device exports (incl. Strava CSV)
- [`wiki/strava-workouts.md`](../../../wiki/strava-workouts.md) - synthesized Strava summary when present
- [`health/AGENTS.md`](../../../health/AGENTS.md) - folder guide only (not an index)
- Other content folders via skill `brain-search`

Do **not** keep a skill-bundled food macro table. Regional and personal food
context lives in [`ABOUT.md`](../../../ABOUT.md) and prior meal notes (via
`brain-search`).

### Nutrition rules

Prefer evidence-based dietary advice aligned with major guidelines.

**Never promote:** miracle diets, detoxes, unsupported supplements, extreme
caloric restriction or dangerous fasting, elimination diets without medical
indication.

Separate **evidence-based recommendations** from **experimental approaches**
(label experimental clearly).

### Required output format (advice)

Every non-emergency advice reply includes these sections (RU or EN to match user):

```markdown
## Assessment
<brief situation summary>

## Confidence
**Confidence:** X%
<why this level>

## Potential Risks
<harm if recommendation is wrong>

## Recommendation
<conservative, evidence-based; tag Low/Medium/High Risk>

## Alternatives
<safer options when uncertainty exists>

## When to See a Doctor
<symptoms or situations needing evaluation>

## Questions
<missing information that would raise confidence>
```

Keep proportional - simple questions get shorter sections; do not pad.

### Safety overrides

When uncertain: prefer observation, consultation, monitoring, and reversible
options over intervention, self-treatment, or drastic irreversible changes.

Always state what is known, uncertain, and assumed. Never pretend to know.

### Estimation safety (BJU / kcal)

When estimating macros or calories (including in **log** mode):

- Label numbers as **estimates**, not medical prescriptions
- Do not treat estimates as clinical targets without context
- If diabetes, eating-disorder history, pregnancy, or other high-stakes context -
  apply **Medium/High Risk** framing and suggest professional guidance for targets

### Advice checklist

- [ ] Evidence tier stated where a claim is made
- [ ] Confidence % given with rationale
- [ ] Recommendation risk class stated (Low/Medium/High/Emergency)
- [ ] Red flags ruled in or escalated
- [ ] Missing personalization listed under Questions if still needed
- [ ] No fabricated studies, diagnoses, or dosages
- [ ] Alternatives and When to See a Doctor included when not Emergency-only

---

## Mode: log (meal logging)

### Scope

Apply when the user attaches or pastes food/meal photos, or explicitly asks to
log a meal.

Do **not** wait for "audit" or "log". Run the full workflow end-to-end.

Do **not** use for non-food images or when the user says not to log / estimate.

### Photos are not saved

Meal photos stay in the chat. Do **not** copy them into `health/` and do **not**
search the filesystem for an attachment path.

- Default note line: `Photo sent in chat; not saved to health/ (photos are not archived).`
- Existing images under `health/` stay as they are
- Exception: if the user gives a real file path, save it as `YYYY-MM-DD-slug.ext`
  (ASCII `-`, no spaces) and link it from the meal note body

### Times are UTC

Meal times come from the message timestamp (UTC). Timezone context, if needed,
comes from [`ABOUT.md`](../../../ABOUT.md) - do not hardcode a region here.

- Write times as `HH:MM UTC` in the meal note and the audit note
- Do not convert to local time unless ABOUT.md says otherwise
- If the user states a time explicitly, record that value and mark it `local`

### Workflow

1. **Branch** - if creating new files while on `main` / `master`, create/check
   out a feature branch first (skill `brain-github`).
2. **Dedupe gate** - before writing anything:
   - `brain-search` / list `health/YYYY-MM-DD-meal-*.md` and
     `health/YYYY-MM-DD-drink-*.md` for the meal date
   - List `.audit/` for `YYYY-MM-DD - *` (`Meal - ` / `Drink - `) when present
   - Same occasion = same date **and** (overlapping dish **or** times within ~90 min)
   - On match: **update** existing meal note + audit note, keep `created`, say
     it was updated
3. **Identify** dish and portions (image + any user text).
4. **Estimate** protein / fat / carbs (g) and kcal:
   - Read [`ABOUT.md`](../../../ABOUT.md) for region / diet / known recurring foods
   - Prefer product labels and prior meal notes for the same dish when present
     (`brain-search` in `health/`)
   - Otherwise estimate from portion; do not invent a vault-wide macro table
   - Label as estimates; ask only if the photo is too ambiguous
   - Apply **Estimation safety** above
5. **Log** one Markdown note under `health/` via skill `brain-add` conventions:
   - Filename: `YYYY-MM-DD-meal-<slug>.md` or `YYYY-MM-DD-drink-<slug>.md`
     (no spaces)
   - Frontmatter required: `title`, `description`, `status: active`,
     `tags: [health, personal]`, `created`
   - Body: time, dish/portions, P/F/C + kcal (estimates), photo line
   - Do **not** write meals into `health/AGENTS.md` and do not create an index
6. **Day total** - sum P/F/C + kcal from all meal/drink notes for that date under
   `health/` (from note bodies). Report the running total in the reply; do not
   maintain a separate totals file.
7. **Audit** - create `.audit/YYYY-MM-DD - Meal - Short Title.md` via
   `brain-audit`:
   - `tags: [personal]`
   - `categories: [health]`
   - Body: what was eaten, BJU + kcal, link to the `health/` meal note
   - Then `brain-fix` Step 1 on that note
8. **Reply** - meal, P/F/C + kcal, day's running total, paths to the meal note
   and audit note.

### Meal note shape

```markdown
---
title: Meal - short name
description: Estimated macros for this meal
status: active
tags:
  - health
  - personal
created: YYYY-MM-DD
---

## Meal

- Time: HH:MM UTC
- Dish: ...
- Protein g / Fat g / Carbs g / kcal: ... (estimates)
- Photo: Photo sent in chat; not saved to health/ (photos are not archived).
```

### Log checklist

- [ ] Dedupe gate run before writing
- [ ] Dish + portions identified
- [ ] Region/diet context from `ABOUT.md` / prior meal notes when available
- [ ] BJU + kcal estimated (labeled as estimates)
- [ ] One `health/YYYY-MM-DD-meal-*.md` (or drink) note created/updated
- [ ] Day total summed from that date's meal notes (reply only)
- [ ] Did not write meals into `AGENTS.md` or create an index file
- [ ] Audit note created via `brain-audit` when applicable
- [ ] Short summary returned, including the daily total

---

## Mode: strava (activity processing)

### Scope

Apply when the user asks to process / analyze / refresh Strava activities,
workouts export, or update the workout wiki page from a Strava CSV.

Do **not** invent activity numbers. Prefer the analyzer script over hand-rolled
tables. Raw CSV stays in `sensors/`; the synthesized page belongs in `wiki/`.

### Placement

| Artifact | Location | Notes |
|----------|----------|-------|
| Strava export CSV | `sensors/` | Prefer `strava-activities.csv` (see [`sensors/AGENTS.md`](../../../sensors/AGENTS.md)) |
| Synthesized summary | `wiki/strava-workouts.md` | Frontmatter via script / `brain-add` conventions |

### Script

[`scripts/strava_analyze.py`](./scripts/strava_analyze.py)

```bash
# From vault root - discover sensors/*strava*.csv and write wiki page
python3 .cursor/skills/brain-health/scripts/strava_analyze.py --out wiki/strava-workouts.md

# Explicit paths
python3 .cursor/skills/brain-health/scripts/strava_analyze.py \
  --csv sensors/strava-activities.csv --out wiki/strava-workouts.md

# Body only (stdout) for chat preview
python3 .cursor/skills/brain-health/scripts/strava_analyze.py --stdout
```

Accepts Russian and English Strava column names / date formats. On `--out`,
preserves existing `created:` when updating the wiki note.

### Workflow

1. **Branch** - if creating `wiki/strava-workouts.md` (or a new CSV under
   `sensors/`) while on `main` / `master`, create/check out a feature branch
   first (skill `brain-github`).
2. **Locate CSV** - prefer path the user gave; else look under `sensors/` for
   `strava-activities.csv` / `strava_activities.csv` / `*strava*.csv`. If
   missing, ask the user to drop the export into `sensors/` (no spaces in the
   filename).
3. **Sanitize name** - if the CSV filename has spaces, rename per
   `brain-form` Step 2 / sensors naming before analyzing.
4. **Run analyzer** with `--out wiki/strava-workouts.md` (create or update).
5. **Verify** - read the wiki note frontmatter (`title`, `description`,
   `status`, `tags` including `wiki`, `created`, `source`). Do **not** append
   anything to `sensors/AGENTS.md` or `wiki/AGENTS.md`.
6. **Reply** - short headline (activity count, date range, total km / hours),
   path to the CSV and wiki page, and how to refresh after the next export.
7. **Advice handoff** - if the user also asked for training/nutrition advice,
   continue in **advice** mode using the wiki summary + `ABOUT.md` (do not
   re-parse the full CSV by hand).

### Strava checklist

- [ ] CSV found or requested under `sensors/`
- [ ] Filename has no spaces
- [ ] Feature branch if creating new tracked files on `main` / `master`
- [ ] `strava_analyze.py --out wiki/strava-workouts.md` succeeded
- [ ] Wiki note has valid frontmatter; `created` preserved on update
- [ ] Did not write inventories into hub `AGENTS.md`
- [ ] Short summary + paths returned to the user

---

## Interaction with other skills

| Skill | Rule |
|-------|------|
| `brain-critical` | User asserts a health conclusion as settled - optional **probe** |
| `brain-search` | Find vault health / wiki / sensors notes before personalizing advice |
| `brain-audit` | Meal log may create `.audit/` events; do not auto-log advice chats or Strava refreshes |
| `brain-add` | Persist protocols to `health/` or `manual/` only when user asks; Strava wiki page is written by the analyzer (same frontmatter rules) |
| `brain-form` | Step 1 on new `.audit/` meal notes; Step 2 if Strava CSV filename has spaces |

## Constraints

- Use `-` not em/en dashes in markdown output
- Do not moralize or shame about food, weight, or illness
- Do not block explicit user instructions with endless questions - ask the
  **minimum** missing facts needed for a safe answer
- When vault medical data is absent, say so - do not assume normal labs or health
- One meal = one note under `health/` (never a shared meal log file)
- Strava raw exports stay in `sensors/`; synthesized tables go to `wiki/`
