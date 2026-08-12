---
name: brain-clarity
description: >-
  Split a piece of text (venting, journal entry, message, recap of a
  conversation or event) into Facts / Opinions / Emotions, each tagged with
  who said it. A parsing pass over raw narrative - not a challenge to a
  conclusion. Use when the user asks to separate facts from opinions/
  feelings, "is this a fact or how I feel", pastes an emotionally charged
  message or recap, journals about a conflict or hard decision, or names
  brain-clarity. Feeds a cleaner input into brain-critical, brain-audit, or
  brain-add when narrative and feeling are tangled together.
---

# Brain Clarity - facts vs opinions vs emotions

## What this is

A lightweight parsing pass over **raw text** - a message, a vent, a recap of
what happened, a journal draft - that sorts every claim into exactly one of
three buckets: **Fact**, **Opinion**, or **Emotion**. It does not judge
whether a fact is true or a conclusion is sound; it only untangles what kind
of statement each sentence actually is.

Not the same as `brain-critical`:

| | `brain-clarity` | `brain-critical` |
|---|---|---|
| Input | Raw narrative, message, vent, recap | A stated conclusion/claim treated as settled |
| Output | Fact / Opinion / Emotion buckets, per statement | Confidence %, killer questions, counterargument |
| Question asked | "What kind of statement is this?" | "Is this conclusion likely to be wrong?" |
| Stance | Neutral sorter | Stress-tester |

Run `brain-clarity` first when the raw input is a tangle of what-happened +
judgment + feeling; hand the resulting **Facts** list to `brain-critical` next
if the user then wants the conclusion itself challenged.

## When to run

| Trigger | Action |
|---------|--------|
| User explicitly asks to separate facts from opinions/feelings, or "is this fact or opinion/emotion" | Run on the text they gave |
| User pastes a message from someone else (complaint, feedback, argument) and asks to make sense of it | Run on that message |
| User vents about a conflict, decision, or event with visible emotional charge **and** asks for help thinking about it (not just to be heard) | Offer/run before advice |
| Before `brain-audit` logs an emotionally charged event and the user wants a clean **What happened** section | Run first, feed Facts into the note body, keep feeling in `mood` field only |
| Before `brain-add` writes a note (e.g. `career/`, `social/`) from a mixed narrative | Run first so the note body stays factual and opinions/feelings are labeled, not silently baked in |
| Explicit name `brain-clarity` | Run in whichever mode fits |

### When to skip

- Text is already purely factual (dates, numbers, a to-do list) - nothing to sort
- User just wants to vent and be heard, with no request to think it through - respect that; do not impose analysis uninvited (one line offering it is fine, do not force the split)
- Text is a single short sentence with an obvious single type - state the type in one line instead of a full table
- User already ran `brain-critical` on the same material in this thread and just wants the challenge, not the sort

## Definitions

| Type | Test | Signals |
|------|------|---------|
| **Fact** | Verifiable, observable, would not change if described by someone else present | Dates, numbers, quotes, actions taken, who/what/when/where |
| **Opinion** | A judgment, interpretation, evaluation, or prediction - could reasonably be argued differently | "should", "always/never", "the problem is", "clearly", "means that", ratings, blame, comparisons |
| **Emotion** | A feeling state, the speaker's or someone else's affect - not a claim about the world | "I feel...", "I'm angry/anxious/relieved", tone words, exclamation-driven venting, physical stress markers |

Edge cases:

- **"He said X"** is a fact about what was said, even if X itself is an opinion. Split the wrapper (fact: he said it) from the content (opinion: X).
- **Mixed sentences** ("He was late again, typical of him") - split into fact ("he was late") + opinion ("typical of him").
- **Reported feelings** ("She seemed upset") is the speaker's *interpretation* of someone else's emotion → opinion, not emotion, unless the other person stated their feeling directly ("she said she was upset" → fact that she said it, plus her emotion attributed to her).
- Attribute every line to **who** said/felt it (self, the other person, a third party) when more than one voice is present.

## Workflow

1. Read the text once fully; do not analyze mid-read.
2. Go sentence by clause, assign exactly one bucket per atomic claim (split
   compound sentences per Edge cases above).
3. Attribute each line to a speaker when more than one person appears.
4. Group into the three buckets, preserving original wording (light editing
   for brevity is fine; do not add claims that were not in the text).
5. If the user's goal is a decision or note, add one short **Facts only**
   recap line at the end - the minimal ground truth to build on.
6. Do not resolve, judge, or rank the opinions/emotions - `brain-critical`
   or `brain-soul` handle evaluation, not this skill.

## Output shape

```markdown
## Facts

- ...

## Opinions / interpretations

- ... (- *speaker*, if more than one voice)

## Emotions

- ... (- *speaker*, if more than one voice)

## Ground truth (facts only)

...one or two sentences, facts alone...
```

Omit a section only if it is genuinely empty (do not force a fake entry).
Skip the **Ground truth** recap for a single-sentence input.

## Interaction with other skills

| Skill | Rule |
|-------|------|
| `brain-critical` | Hand the **Facts** bucket forward as the claim's factual base; brain-critical then runs its own Facts/Interpretation/Action split on the *conclusion*, not the raw narrative |
| `brain-audit` | Facts feed the **What happened** section; emotional content maps to the `mood` field, not free text mixed into facts |
| `brain-add` / `social/`, `career/` notes | Keep note bodies to facts + explicitly labeled opinions; do not silently launder opinion as fact |
| `brain-soul` | Soul may add an opinion *after* the split - do not let soul's own opinion contaminate the neutral sort itself |
| Task execution | If the user only wants to vent, acknowledge first; offer the split rather than forcing it |

## Constraints

- Never invent facts, opinions, or emotions not present in the source text
- Never silently upgrade an opinion to a fact (or the reverse)
- Preserve who said what when multiple people are quoted
- Stay neutral - this skill sorts, it does not judge who is right
- Keep buckets proportional to input length; do not pad short input into a long table
- Use `-` not em/en dashes in markdown output

## Checklist

Before finishing:

- [ ] Every sentence/clause assigned to exactly one bucket (or split when compound)
- [ ] Speaker attribution present when more than one voice appears
- [ ] No claim invented beyond the source text
- [ ] Opinions and emotions not smuggled into the Facts bucket
- [ ] Ground truth recap added when the user's goal is a decision or a note (skipped for one-liners)
- [ ] Empty buckets omitted rather than faked
