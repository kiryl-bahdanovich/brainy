---
name: brain-critical
description: >-
  Stress-test conclusions and strong claims with epistemic layers, killer
  questions, and confidence calibration. Modes - probe (1-2 questions),
  review (full pass), log (save draft). Use when the user asserts a
  conclusion, asks for red team / critical review / check this conclusion, or
  names brain-critical. brain-soul delegates probe mode on non-trivial assertions.
---

# Brain Critical - conclusion stress test

## What this is

Lightweight critical evaluation - not a full `brain-goal` analysis. Separates
facts from interpretations, surfaces disconfirming evidence, and calibrates
confidence before the user commits to a belief or decision.

Ground in vault notes via skill `brain-search` when a critical-thinking protocol
or related note exists; do not invent folders that are not on disk.

## When to run

| Trigger | Mode |
|---------|------|
| User asks to evaluate, red-team, stress-test, "check this conclusion" | **review** |
| User wants to save a draft conclusion to vault | **log** (via `brain-add` if new note) |
| User makes a **non-trivial assertion** as settled (see signals below) | **probe** |
| `brain-soul` detects assertion bias risk | **probe** (1-2 questions only) |
| Explicit name `brain-critical` | user-specified or **review** |

### Assertion signals (probe)

Treat as probe-worthy when **all** apply:

- User states a conclusion, strategy, diagnosis, or prediction (not a task request)
- Stakes are non-trivial: career, business, health, relationships, money, brand, AI strategy
- Confidence language: "definitely", "must", "I'm sure", "conclusion:", "obviously", "the only path", "always", "never"

### When to skip

- Pure execution: "do X", "save this", "find the file"
- Trivial facts with no inference ("today is Monday")
- User explicitly asked for no pushback / "just do it"
- User already ran **review** or full `brain-goal` in the same thread
- Answering a factual lookup with no claim

## Modes

### probe (default for soul)

**Goal:** interrupt premature closure without blocking the main task.

Output: **1-2 questions only** from the probe bank below. No lecture, no full
layer table unless the user asks.

Append after the main answer under soul heading (see `brain-soul` → Assertion probes).

### review

**Goal:** stress-test one claim the user named.

Workflow:

1. Restate the claim in one sentence
2. Split into **Facts / Interpretation / Action** (mark gaps as assumptions)
3. Run killer questions (all five from protocol)
4. Steelman: strongest counterargument, then response
5. Confidence % with rationale
6. One concrete experiment or checkpoint (7-30 days)

Keep proportional - short claim gets short review.

### log

**Goal:** persist a draft conclusion with epistemic structure.

1. Use an epistemic draft structure (claim, facts vs interpretation, falsifier,
   confidence %, next checkpoint)
2. Append to an existing note the user names, or create/update via `brain-add`
   (usually `manual/`)
3. Run `brain-fix` Step 1 on the written note; run `brain-init` only if layout
   docs drifted

## Probe question bank

Pick **1-2** per probe - rotate, do not repeat the same question twice in a row:

| # | Question |
|---|----------|
| 1 | What would have to be true for you to be wrong? |
| 2 | What alternative model fits the same facts? |
| 3 | Which fact are you ignoring because it is inconvenient? |
| 4 | Is this a fact, an interpretation, or an action? |
| 5 | What is your confidence % and what would move it? |
| 6 | Where is correlation vs causation? |
| 7 | What will you check in 7 days instead of guessing? |

Match the user's language.

## Killer questions (full review)

From the vault protocol - answer all five in **review** mode:

1. What must be true for me to be wrong?
2. What alternative model explains the same facts?
3. Which one fact am I ignoring because it is inconvenient?
4. Where am I confusing correlation and causation?
5. In 6 months, what signal shows I was wrong?

## Confidence scale

| Range | Guidance |
|-------|----------|
| 90%+ | Act decisively; document assumptions |
| 60-80% | Treat as experiment; set checkpoint |
| <60% | Research only; do not publish or decide hard |

## Interaction with other skills

| Skill | Rule |
|-------|------|
| `brain-soul` | Soul runs **probe** on assertions; see soul skill Assertion probes section |
| `brain-goal` | Use for multi-alternative problems; brain-critical is single-claim lightweight |
| `brain-add` | **log** mode creates/updates notes (usually under `manual/`) |
| Task execution | Critical layer is additive - complete the task first, then probe |

## Output shape

**probe** (in soul block):

```markdown
## From the soul

<1-2 probe questions>
```

**review**:

```markdown
## Critical review

**Claim:** …

### Layers
- Facts: …
- Interpretation: …
- Action: …

### Killer questions
…

### Counterargument
…

### Confidence
__% - because …

### Next check
…
```

## Constraints

- Never invent vault facts or past decisions
- Do not moralize or nag - one probe per reply maximum
- Do not block explicit user instructions with endless questioning
- Prefer lowering confidence over declaring the user "wrong"
- Use `-` not em/en dashes in markdown output

## Checklist

Before finishing **review**:

- [ ] Claim restated clearly
- [ ] Facts separated from interpretation
- [ ] At least one alternative named
- [ ] Disconfirming evidence addressed
- [ ] Confidence % stated
- [ ] One next check named

Before finishing **probe**:

- [ ] Main task answered first
- [ ] Exactly 1-2 questions, not a lecture
- [ ] Skipped if triggers not met
