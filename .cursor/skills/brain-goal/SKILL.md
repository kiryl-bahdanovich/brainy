---
name: brain-goal
description: >-
  Systematic expert problem-solving using vault notes in personal data folders
  (calendar, career, documents, finance, health, internet, manual, media,
  social, statistics). Apply multiple parallel thinking approaches (First
  Principles, Analogies, Decomposition, Theory of Constraints, Inversion,
  Design Thinking, Experimental, Systems Thinking) to explore the solution
  space, generate distinct alternatives, critically evaluate them, and
  recommend the best path with full logical reasoning. Discover notes via
  brain-search (hub + frontmatter only). Search internet when vault is
  insufficient.
---

# Brain Goal - Systematic Problem Solving

## Scope

**Primary sources** (read first):

| Source | Role |
|--------|------|
| [`ABOUT.md`](../../../ABOUT.md) | Priorities and how to work with the user |
| Content hubs via skill `brain-search` | Notes with YAML frontmatter in personal data folders |
| Folder `AGENTS.md` guides | Placement boundaries when choosing hubs |

Personal data hubs (same as `brain-search` / `brain-add`):

- `calendar/`, `career/`, `documents/`, `finance/`, `health/`
- `internet/` (saved web clips), `manual/` (self-authored notes)
- `media/`, `social/`, `statistics/`

**Fallback** (when vault is insufficient):

- Internet search via WebSearch tool

**Output**:

- Present analysis directly to the user with full logical flow
- Optionally save under `manual/` via skill `brain-add` if the user asks

Do **not** invent folders that are not on disk. Do not use chat history alone
or external repos as primary sources. Never guess or invent vault paths.

## Goal

You are an expert in systematic complex problem solving. Given a user's problem
statement, analyze it using multiple parallel thinking approaches, critically
evaluate all alternatives, and recommend the best solution with complete logical
reasoning and vault sources.

## Framework Overview

1. **Problem Clarification** - define the real problem vs symptoms
2. **Parallel Solution Search** - explore 8 independent approaches simultaneously
3. **Synthesis of Alternatives** - generate 3-5 truly distinct solutions
4. **Critical Thinking** - rigorously challenge each alternative
5. **Comparison Matrix** - score alternatives across key dimensions
6. **Final Recommendation** - select the best path with justification
7. **Action Plan** - concrete next steps with checkpoints

## Workflow Checklist

```
Problem-solving progress:
- [ ] Clarify the problem (real problem vs symptoms, stakeholders, success criteria)
- [ ] Read ABOUT.md for priorities / work preferences
- [ ] Inventory vault via brain-search (hub-first, frontmatter-only match)
- [ ] Read bodies of promising matches only (after frontmatter hit)
- [ ] Apply 8 parallel approaches
- [ ] Check vault sufficiency: search internet if gaps exist
- [ ] Synthesize 3-5 distinct alternatives (not variations)
- [ ] Critical review: challenge assumptions, identify biases, find counterarguments
- [ ] Compare alternatives in matrix
- [ ] Select best solution with clear justification
- [ ] Define action plan (now, 7 days, 30 days, checkpoint)
- [ ] Present full analysis with sources
- [ ] Optionally save under manual/ via brain-add if requested
```

### Step 1: Problem Clarification

The user will provide a problem/goal statement with optional context and constraints.

**Define:**

- **Real problem** - what truly needs to be solved (not just symptoms)
- **Stakeholders** - who cares and why
- **Success criteria** - measurable outcomes that define success
- **Known facts vs assumptions** - separate certainties from hypotheses
- **Information gaps** - what's missing; make reasonable assumptions and mark them explicitly

**Examples:**

- "Find ways to advance my AI career while maintaining work-life balance"
- "Build a personal brand in delivery management"
- "Start a consulting business without burning out"
- "Learn Kubernetes for production use"

**Extract:**

- **Core objective** - the desired outcome
- **Constraints** - explicit or implicit limits (time, resources, priorities)
- **Context** - career stage, current situation, related priorities from vault

Refer to [`ABOUT.md`](../../../ABOUT.md) priorities when interpreting goals
without explicit priorities. If ABOUT is still TBD, say so and ask or mark
assumptions - do not invent a priority order.

When information is insufficient, make reasonable assumptions and clearly mark them.

### Step 2: Inventory Vault Sources & Parallel Solution Search

**First**, gather vault knowledge (hub + frontmatter only to find candidates):

1. Read [`ABOUT.md`](../../../ABOUT.md).
2. Map the problem to one or more **content hubs** (folder placement from root
   [`AGENTS.md`](../../../AGENTS.md)):

   | Problem theme | Prefer hubs |
   |---------------|-------------|
   | Career / brand / business | `career/`, `manual/` |
   | Money / runway | `finance/`, `career/` |
   | Health / energy | `health/`, `manual/` |
   | People / relationships | `social/` |
   | Schedule / capacity | `calendar/` |
   | External evidence / clips | `internet/`, `statistics/` |
   | Own decisions / journals | `manual/` |

3. Use skill `brain-search` (frontmatter script) - do **not** body-scan the vault
   to discover notes:

```bash
python3 .cursor/skills/brain-search/scripts/search_frontmatter.py --hub career <keywords...>
python3 .cursor/skills/brain-search/scripts/search_frontmatter.py --hub manual --hub internet <keywords...>
```

   Prefer `active` and `draft` over `archived`. Expand to all hubs (omit `--hub`)
   only if scoped search is too narrow or empty.
4. **Only then** read bodies of promising matches (aim for 5-15 relevant sources).
5. Track sources: save paths and key insights from each. Skip `AGENTS.md` as a
   "note" source unless citing a placement rule.

**Then**, explore the problem through **8 parallel approaches** simultaneously:

#### A. First Principles

Decompose the problem to fundamental facts and constraints. Build the solution
from ground up without relying on existing practices. Ask:

- What are the immutable physical/logical/economic laws here?
- What if we ignore current practices and rebuild from basics?
- What assumptions can we discard?

**Use vault sources** for foundational facts and constraints.

#### B. Analogies and Existing Practices

Find similar problems in other companies, products, industries, or systems:

- What analogous problems have been solved elsewhere?
- Which solutions can be adapted?
- Where might the analogy break down?

**Search vault** for past experiences, case studies, industry examples
(`internet/`, `statistics/`, `manual/`, `career/`).
**Search internet** if vault lacks analogies.

#### C. Decomposition

Break the problem into smaller independent parts. Solve each part separately,
then integrate:

- What are the sub-problems?
- Can they be solved independently?
- How do the pieces combine into a whole solution?

**Use vault notes** to map dependencies and modular solutions.

#### D. Theory of Constraints

Find the primary bottleneck limiting the outcome:

- What single constraint causes the most limitation?
- What happens if we remove or relax only this constraint?
- Which bottleneck should we tackle first?

**Vault sources** may reveal historical bottlenecks or current blockers.

#### E. Inversion

Think backwards - what would guarantee failure?

- What actions would make the situation worse?
- What mistakes must we avoid?
- How can we minimize the worst-case scenario?
- What would make this a certain disaster?

**Check vault** for past failures, lessons learned, anti-patterns (`manual/`,
`career/`).

#### F. Design Thinking

Consider the problem from the user's/stakeholder's perspective:

- What are their real needs and pain points?
- What creates value for them?
- What solution would be convenient and understandable in practice?

**Vault sources** may contain user feedback, stakeholder priorities, usability
insights (`social/`, `career/`, `manual/`).

#### G. Experimental Approach

Propose minimal, low-cost experiments to test key hypotheses before large
investments:

- What are the riskiest assumptions?
- What quick experiments can validate or invalidate them?
- How can we learn fast and cheaply?

**Look in vault** for past experiments, MVPs, pilot results.

#### H. Systems Thinking

Analyze second-order effects, dependencies, feedback loops:

- What are the direct and indirect consequences?
- How does this solution affect other parts of the system?
- What feedback loops exist?
- What happens 3, 6, 12 months later?

**Vault notes** may document system interactions, long-term outcomes, cascading
effects. Cross hubs when the question spans career / health / money / time.

### Step 3: Synthesis of Alternatives

Based on the 8 parallel approaches, synthesize **3-5 truly distinct solution
variants**. Do NOT create minor variations of the same approach.

For each variant, specify:

- **Essence** - core idea in 1-2 sentences
- **Expected value** - what outcome it produces
- **Advantages** - strengths
- **Disadvantages** - weaknesses
- **Cost and effort** - technical complexity and scope (not calendar time)
- **Speed to result** - how fast it delivers value
- **Key risks** - failure modes
- **Reversibility** - can it be undone?
- **Required assumptions** - what must be true for this to work
- **Best conditions** - when this variant is optimal
- **Vault sources** - which notes/insights support this variant

**Format:**

```markdown
## Variant A: <Short Name>

**Essence**: <1-2 sentence summary>

**Approach**:
- Step 1
- Step 2
- Step N

**Expected value**: <outcome>

**Advantages**: <strengths>

**Disadvantages**: <weaknesses>

**Cost & effort**: <complexity, not time>

**Speed**: <fast/medium/slow to deliver value>

**Key risks**: <failure modes>

**Reversibility**: <high/medium/low - can it be undone?>

**Assumptions**: <what must be true>

**Best when**: <optimal conditions>

**Vault sources**:
- `manual/YYYY-MM-DD-topic.md` - <insight>
- `career/YYYY-MM-DD-review.md` - <insight>
- `internet/YYYY-MM-DD-source-slug.md` - <insight>
```

Ensure variants are **genuinely different**, not cosmetic variations.

### Step 4: Critical Thinking Review

For each variant, conduct rigorous critical review:

**Challenge assumptions:**

- Which claims lack sufficient evidence?
- Which assumptions might be wrong?
- What cognitive biases might affect the conclusion?
- What important alternatives might have been missed?
- What stakeholder interests might distort the decision?
- Where is correlation mistaken for causation?

**Find counterarguments:**

- What are the strongest arguments **against** this variant?
- What could prove this solution wrong?
- What unexpected scenario could lead to failure?
- Is the solution more complex than the problem itself?

**Play the strong opponent** - try to disprove the preliminary conclusions.

**Evaluate:**

- **Feasibility** - can it be done given constraints?
- **Alignment** - does it match ABOUT.md priorities (when set)?
- **Impact** - what outcomes does it produce?
- **Effort** - technical complexity, scope (never calendar time)
- **Dependencies** - what must exist or happen first?
- **Risks** - failure modes, trade-offs, downsides

Think step-by-step. Surface conflicts between priorities (e.g., career vs
work-life balance). Be honest about difficulty.

When the recommendation is a strong settled claim, skill `brain-critical`
(probe) and/or `brain-soul` may apply - do not skip critical review here.

### Step 4.5: Internet Research (if vault is insufficient)

After exploring vault sources, assess gaps:

- Are there unknowns that vault doesn't address?
- Does the user need current/external information (tools, market trends, best practices)?
- Would additional context improve alternatives or evaluation?
- Is the vault empty or nearly empty for this topic? Say so explicitly, then search.

If yes, use **WebSearch** to fill gaps:

```
Search queries examples:
- "<domain> best practices 2026"
- "how to <action> while <constraint>"
- "<tool> production setup guide"
- "<career path> typical progression"
```

Integrate web findings into variants and critical review. Track URLs as sources.

### Step 5: Comparison Matrix

Score variants on a 1-10 scale across key dimensions. For **cost** and **risk**,
higher score means better (lower cost, lower risk).

| Variant | Impact | Cost | Speed | Risk | Scalability | Reversibility | Confidence |
|---------|--------|------|-------|------|-------------|---------------|------------|
| A       | 8      | 6    | 7     | 5    | 9           | 8             | 7          |
| B       | 6      | 8    | 9     | 7    | 6           | 9             | 8          |
| C       | 9      | 4    | 5     | 4    | 8           | 5             | 6          |

**Do NOT create false mathematical precision.** Explain what each score is based on.

**Dimensions:**

- **Impact** - how much value it creates
- **Cost** - effort/resources (10 = lowest cost)
- **Speed** - how fast it delivers results
- **Risk** - failure probability (10 = lowest risk)
- **Scalability** - can it scale beyond initial scope?
- **Reversibility** - can it be undone if wrong?
- **Confidence** - how confident are we in the analysis?

### Step 6: Final Recommendation

Give a concrete answer:

1. **Which solution do you recommend?**
2. **Why is it better than alternatives?** - clear justification
3. **Under what assumptions is this recommendation valid?** - mark prerequisites
4. **When should you choose a different variant?** - conditions for switching
5. **What must NOT be done?** - anti-patterns, traps to avoid
6. **What is the first practical step?** - immediate concrete action
7. **How to validate the solution with minimal cost?** - quick tests
8. **What criteria determine continue/pivot/stop?** - decision checkpoints

Be direct: state the recommended path clearly.

### Step 7: Action Plan

Create a practical, time-bound plan:

- **Now** - first immediate step
- **Next 7 days** - validate key hypotheses
- **Next 30 days** - execute or run pilot
- **Checkpoint** - measurable criteria to decide continue/pivot/stop

## Output Format

Structure the final presentation:

```markdown
# Problem: <User's problem statement>

## 1. Problem Clarification

**Real problem**: <what truly needs solving>
**Stakeholders**: <who cares and why>
**Success criteria**: <measurable outcomes>
**Known facts vs assumptions**: <separate certainties from hypotheses>
**Information gaps**: <what's missing; assumptions made>

**Parsed objective**: <goal>
**Constraints**: <limits>
**Context**: <career/situation from vault / ABOUT.md>

## 2. Vault Sources Explored

<Count and summary: "Explored 8 sources across career/ (3), manual/ (4), internet/ (1)">

## 3. Parallel Approaches Applied

Brief summary of insights from each approach:

- **A. First Principles**: <key insight>
- **B. Analogies**: <key insight>
- **C. Decomposition**: <key insight>
- **D. Theory of Constraints**: <bottleneck found>
- **E. Inversion**: <what to avoid>
- **F. Design Thinking**: <user needs>
- **G. Experimental**: <test ideas>
- **H. Systems Thinking**: <second-order effects>

## 4. Solution Variants (3-5)

<Present all variants with full fields and vault sources>

## 5. Critical Review

<For each variant: challenge assumptions, counterarguments, feasibility, alignment, impact, effort, dependencies, risks>

## 6. Comparison Matrix

| Variant | Impact | Cost | Speed | Risk | Scalability | Reversibility | Confidence |
|---------|--------|------|-------|------|-------------|---------------|------------|
| ...     | ...    | ...  | ...   | ...  | ...         | ...           | ...        |

<Explain scoring rationale>

## 7. Internet Research (if used)

<Queries run, key findings, URLs>

## 8. Recommended Solution

**Variant X: <Name>**

1. **Why this solution?** <justification>
2. **Why better than alternatives?** <comparison>
3. **Valid under assumptions:** <prerequisites>
4. **Choose different variant when:** <switching conditions>
5. **What NOT to do:** <anti-patterns>
6. **First step:** <immediate action>
7. **Validation test:** <minimal-cost check>
8. **Decision criteria:** <continue/pivot/stop metrics>

## 9. Action Plan

- **Now**: <immediate step>
- **Next 7 days**: <hypothesis validation>
- **Next 30 days**: <execution/pilot>
- **Checkpoint**: <measurable decision criteria>

## 10. Summary

**Main conclusion**: <one sentence>

**Confidence level**: low / medium / high

**What could most change this recommendation**: <key factor>

## All Sources

**Vault sources**:
- `manual/YYYY-MM-DD-topic.md` - <role in reasoning>
- `career/YYYY-MM-DD-review.md` - <role in reasoning>

**Web sources** (if used):
- [Article title](URL) - <role in reasoning>
```

### Step 8: Save under manual/ (optional)

If the user asks to save the analysis, follow skill `brain-add`:

- Folder: `manual/` (self-authored synthesis)
- Filename: `YYYY-MM-DD-goal-<short-slug>.md` (no spaces)
- Frontmatter required by `brain-add` (`title`, `description`, `status`, `tags`,
  `created`). Include tags `manual` and any cross-cutting tags that apply
  (`career`, `ai`, `business`, …).
- Optional extra keys allowed (preserve on later updates):

```yaml
---
title: <Problem title>
description: <Recommended solution in one sentence>
status: draft
tags:
  - manual
  - career
problem: <Original problem statement>
confidence: medium
created: YYYY-MM-DD
---
```

Body: full analysis following the Output Format.

Respect `brain-github` when creating a **new** file (feature branch, not on
`main` / `master`).

## Constraints

- Primary sources only from on-disk content hubs + `ABOUT.md`
- Discover candidates via `brain-search` (hub + frontmatter); read bodies only after match
- Use WebSearch only when vault is insufficient (or empty for the topic)
- Think deeply: apply all 8 parallel approaches
- Generate 3-5 **truly distinct** variants (not minor variations)
- Critically evaluate: challenge assumptions, find counterarguments
- Be direct: recommend one best path with clear justification
- Track all sources (vault + web)
- Present full structured analysis (10-section format)
- Save to `manual/` via `brain-add` only if the user requests it
- Never guess or invent sources; cite real paths and URLs

## Thinking Guidelines

- **Do NOT jump to one solution** - explore in parallel first
- **Reason hard**: evaluate trade-offs honestly, surface conflicts
- **Think systematically**: 8 independent approaches, not one path
- **Be concrete**: actionable steps, not vague advice
- **Use context**: apply ABOUT.md priorities and the user's vault situation
- **Challenge everything**: assumptions, biases, false precision, correlation vs causation
- **Play strong opponent**: try to disprove your own conclusions
- **Integrate knowledge**: connect vault insights across hubs and variants
- **Separate facts from assumptions**: mark hypotheses explicitly
- **Avoid cognitive biases**: confirmation bias, sunk cost, etc.
- **Think second-order**: what happens 3, 6, 12 months later?

## Checklist

Before finishing:

- [ ] **Problem clarified**: real problem vs symptoms, stakeholders, success criteria, facts vs assumptions
- [ ] **ABOUT.md consulted** (or marked TBD with assumptions)
- [ ] **Vault sources inventoried**: brain-search hub-first + frontmatter-only match
- [ ] **8 parallel approaches applied**
- [ ] **3-5 truly distinct variants synthesized**
- [ ] Each variant has full fields + vault sources with real paths
- [ ] **Critical review completed**
- [ ] **Comparison matrix created** with scoring rationale
- [ ] **Internet search performed** if vault gaps exist
- [ ] **Best solution selected** with justification, assumptions, switching conditions, anti-patterns, first step, validation, decision criteria
- [ ] **Action plan defined**: Now, 7 days, 30 days, Checkpoint
- [ ] **Summary provided**: conclusion, confidence, what could change the call
- [ ] **Full structured analysis presented**
- [ ] **All sources listed** (vault paths + web URLs)
- [ ] **Saved under `manual/` via brain-add** only if requested
