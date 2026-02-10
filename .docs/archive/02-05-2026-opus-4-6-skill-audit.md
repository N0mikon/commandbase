---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Confirmed archive status. Bumped git_commit (was 49 commits behind). Fixed references to reflect current paths. Content left as historical record."
topic: "Opus 4.6 Behavioral Impact on Skills"
tags: [research, audit, opus-4-6, skills, enforcement-patterns]
status: archived
archived: 2026-02-09
archive_reason: "Findings fully consumed by companion plan (02-05-2026-opus-4-6-skill-hardening.md, status: complete). Skills moved from ~/.claude/skills/ to plugins/*/skills/ (22 audited vs 46 now). Audit scope no longer representative."
references:
  - .docs/research/02-05-2026-opus-4-6-vs-4-5-changes.md
  - plugins/*/skills/*/SKILL.md
---

# Opus 4.6 Skill Audit: Behavioral Impact Analysis

**Date**: February 5, 2026
**Scope**: All 22 skills in ~/.claude/skills/
**Method**: Standard 5-category validation audit + behavioral risk assessment against Opus 4.6 changes
**Prerequisite Research**: .docs/research/02-05-2026-opus-4-6-vs-4-5-changes.md

## TL;DR

All 22 skills pass the standard 5-category structural audit with zero issues. However, three Opus 4.6 behavioral changes create new risks that existing enforcement patterns don't fully address: **verbosity** (longer outputs), **unexpected modifications** (changes without justification), and **stronger persistence** (staying on tasks longer). The existing Iron Law / Gate Function pattern is the correct mechanism to counter these - the gaps are in specific skills that lack explicit constraints for output length and plan adherence.

---

## Standard Audit Results

All 22 skills pass all 5 validation categories:

| Category | Result | Notes |
|----------|--------|-------|
| 1. Frontmatter | 22/22 pass | All have valid YAML with name + description |
| 2. Name | 22/22 pass | All gerund-form, kebab-case, match directory |
| 3. Description | 22/22 pass | All start with "Use this skill when...", under 1024 chars |
| 4. Structure | 22/22 pass | All under 500 lines, SKILL.md at root |
| 5. Enforcement Patterns | 22/22 pass | All have Iron Law, Gate Function, Red Flags, Rationalization Prevention, Bottom Line |

**No structural fixes needed.**

---

## Opus 4.6 Behavioral Changes (from prerequisite research)

Three changes from the Opus 4.6 release are relevant to skill compliance:

| Behavior | Description | Source |
|----------|-------------|--------|
| **Verbosity** | Outputs tend to be longer than Opus 4.5 | Community reports, Every.to blind test |
| **Unexpected modifications** | Makes code changes without clear justification | Reddit, Cursor forum |
| **Stronger persistence** | Greater ability to stay on long tasks | Michael Truell (Cursor CEO) |

Additional context: Opus 4.6 has adaptive thinking (auto-decides reasoning depth) and 128K output tokens (doubled from 64K). Both amplify the verbosity tendency.

---

## Risk Assessment by Skill

### Risk Categories

- **HIGH**: Skill directly produces output or makes changes where the 4.6 behavior is a real concern
- **Medium**: Skill could be affected but existing guardrails partially mitigate
- **Low**: Skill is unlikely to be affected or is already well-guarded

### Full Assessment

| # | Skill | Verbosity | Unexpected Changes | Persistence | Overall |
|---|-------|-----------|--------------------|-------------|---------|
| 1 | bookmarking-code | Low | Low | Low | Low |
| 2 | committing-changes | **HIGH** | Low | Low | **HIGH** |
| 3 | creating-agents | Medium | Low | Low | Medium |
| 4 | creating-prs | **HIGH** | Low | Low | **HIGH** |
| 5 | creating-skills | Medium | Low | Low | Medium |
| 6 | debating-options | Medium | Low | Medium | Medium |
| 7 | debugging-code | Low | Low | **HIGH** | **HIGH** |
| 8 | discussing-features | Low | Low | Low | Low |
| 9 | handing-over | Medium | Low | Low | Medium |
| 10 | implementing-plans | Medium | **HIGH** | **HIGH** | **HIGH** |
| 11 | learning-from-sessions | Medium | Low | Low | Medium |
| 12 | planning-code | Medium | Low | Medium | Medium |
| 13 | researching-code | Medium | Low | Medium | Medium |
| 14 | researching-web | Medium | Low | Medium | Medium |
| 15 | reviewing-changes | Medium | Medium | Low | Medium |
| 16 | reviewing-security | Low | Low | Low | Low |
| 17 | starting-projects | Medium | Low | Low | Medium |
| 18 | taking-over | Low | Low | Low | Low |
| 19 | updating-claude-md | Low | Medium | Low | Medium |
| 20 | updating-skills | Low | Low | Low | Low |
| 21 | validating-code | Low | Low | **HIGH** | **HIGH** |
| 22 | (audit covers all) | - | - | - | - |

**HIGH risk skills**: committing-changes, creating-prs, debugging-code, implementing-plans, validating-code

---

## Detailed Findings by Risk Category

### 1. Verbosity Risk

**What changed**: Opus 4.6 produces longer outputs. Community consensus and blind testing confirm this.

**Skills with output length concerns**:

#### committing-changes
- **Current guardrail** (line 117-120): "Keep first line under 72 characters"
- **Gap**: No constraint on commit message body length. No "be concise" instruction for the message itself.
- **Risk**: Bloated multi-paragraph commit messages where a single line would suffice.
- **Proposed fix**: Add explicit body length guidance: "Body should be 0-3 bullet points. If you need more, the commit is too large - split it."

#### creating-prs
- **Current guardrail** (line 99-103): "Be concise but thorough"
- **Gap**: No word or line limits on PR description sections. "Concise but thorough" is subjective.
- **Risk**: PR descriptions that are walls of text, especially the Summary and Changes sections.
- **Proposed fix**: Add explicit limits: "Summary: 1-3 bullet points. Changes: 2-5 sentences. Testing: 1-3 bullets. Notes: only if needed."

#### handing-over
- **Current guardrail** (line 186-210): "Bullet points over paragraphs", "Aim for clarity, not length"
- **Assessment**: Well-guarded. The explicit "bullet points over paragraphs" instruction is a strong anti-verbosity measure.
- **Risk**: Low. Existing guardrails are sufficient.

#### reviewing-changes
- **Current guardrail** (line 97-103): Structured commit message template with type prefix
- **Gap**: No max length on the commit message draft.
- **Risk**: Medium. The structured format helps constrain output.
- **Proposed fix**: Mirror committing-changes fix.

### 2. Unexpected Modifications Risk

**What changed**: Opus 4.6 makes code changes without clear justification. Users report unsolicited refactoring and modifications.

**Skills with modification concerns**:

#### implementing-plans (PRIMARY CONCERN)
- **Current guardrail** (line 56-62): "Follow the plan's intent while adapting to what you find"
- **Gap**: The word "adapting" gives license for exactly the behavior Opus 4.6 exhibits. No Red Flag for "making changes not described in the plan."
- **Risk**: HIGH. This is the skill most likely to trigger Opus 4.6's tendency to make unsolicited changes. The plan says "add function X" and 4.6 also refactors function Y "while it's there."
- **Proposed fix**:
  1. Add Red Flag: "Making changes not described in the plan without explaining why and getting approval"
  2. Add Rationalization Prevention row: "This related code could use cleanup" / "Only change what the plan specifies. File a separate task for other improvements."
  3. Tighten the adapt language: "Follow the plan exactly. If reality requires deviation, STOP and present the deviation before making it."

#### updating-claude-md
- **Current guardrail**: Requires showing proposals and getting approval before any change.
- **Assessment**: Well-guarded. The proposal/approval workflow is strong.
- **Risk**: Low. Existing guardrails are sufficient.

#### reviewing-changes
- **Assessment**: Read-only analysis. Cannot make modifications.
- **Risk**: Low.

### 3. Persistence Risk

**What changed**: Opus 4.6 has greater persistence on long tasks. Combined with 128K output tokens, it can work much longer before stopping.

**Skills with persistence concerns**:

#### debugging-code
- **Current guardrail**: Hypothesis tracking, Eliminated section, debug file persistence.
- **Assessment**: Actually well-designed for persistent agents. The hypothesis/elimination loop prevents going in circles. The debug file prevents re-investigating eliminated theories.
- **Risk**: Positive. 4.6's persistence is a feature here, not a bug. The structured investigation loop channels persistence productively.
- **Proposed fix**: None needed. This is a model of good design for persistent agents.

#### implementing-plans
- **Current guardrail** (line 89): "Do NOT pause between phases. Execute all phases continuously until complete or blocked."
- **Gap**: Combined with verbosity and unexpected modifications, persistence means 4.6 will barrel through all phases making verbose, potentially off-plan changes without stopping.
- **Risk**: HIGH. The "don't pause" instruction amplifies both other risks.
- **Proposed fix**: The don't-pause instruction is correct for efficiency, but needs the unexpected-modifications guardrail above to compensate. The Gate Function (line 19-24) requiring fresh verification per phase is the correct checkpoint mechanism.

#### validating-code
- **Current guardrail**: Two-stage gate (spec compliance THEN code quality).
- **Assessment**: Well-guarded. The sequential stage requirement prevents skipping ahead. The "fresh evidence" Iron Law prevents trusting cached results.
- **Risk**: Positive. Persistence helps thoroughness here.
- **Proposed fix**: None needed.

---

## Design Pattern Analysis

### What Works Well Against 4.6 Behaviors

1. **Iron Laws**: The single non-negotiable constraint per skill is the strongest defense. Opus 4.6's tendency to deviate is directly countered by a clear, memorable rule.

2. **Gate Functions**: Sequential numbered steps with "ONLY THEN" at the end force the model through a verified path. This is especially effective against the unexpected-modifications tendency.

3. **Rationalization Prevention tables**: These directly address the excuses Opus 4.6 might generate to justify deviations. The format (Excuse | Reality) is a strong pattern.

4. **Red Flags**: The "STOP and Verify" sections catch exactly the behaviors Opus 4.6 exhibits - proceeding without verification, making assumptions, skipping steps.

### What Needs Strengthening

1. **Explicit output length constraints**: "Be concise" is subjective. "Max 3 bullet points" is concrete. Skills that produce user-facing text need specific limits.

2. **Plan adherence language**: "Adapt to what you find" is too permissive for a model that already tends to make unsolicited changes. Tighten to "Follow the plan. Deviate only when blocked, and explain the deviation."

3. **Scope creep Red Flags**: Skills that modify code (implementing-plans) need an explicit Red Flag for "making changes not described in the plan/task."

### What Doesn't Need Changing

1. **Model-agnostic design**: Skills should NOT contain model-specific language like "Because Opus 4.6 tends to..." The enforcement patterns are the right abstraction.

2. **debugging-code structure**: The hypothesis/elimination loop is excellent design that channels persistence productively.

3. **Approval gates**: Skills that require user approval before changes (updating-skills, updating-claude-md, creating-prs) are naturally resistant to all three 4.6 behaviors.

---

## Recommended Updates (Priority Order)

### Priority 1: implementing-plans
- Add Red Flag for out-of-plan changes
- Add Rationalization Prevention row for scope creep
- Tighten "adapt" language to require explicit deviation reporting
- **Why first**: Highest combined risk (unexpected changes + persistence)

### Priority 2: committing-changes
- Add explicit commit message body length guidance
- **Why second**: Every session ends with a commit; verbosity here has the highest frequency impact

### Priority 3: creating-prs
- Add explicit section length limits to PR description template
- **Why third**: PR descriptions are visible to reviewers; verbosity here has external impact

### Priority 4: reviewing-changes
- Mirror commit message length guidance from committing-changes
- **Why fourth**: Feeds into committing-changes; consistency matters

---

## Methodology Notes

- Standard audit used the 5-category checklist from updating-skills/reference/audit-checklist.md
- Behavioral risk assessment based on community-reported Opus 4.6 behaviors documented in .docs/research/02-05-2026-opus-4-6-vs-4-5-changes.md
- Risk ratings are qualitative assessments based on how directly each skill's workflow intersects with the reported behavioral changes
- "Proposed fixes" are recommendations only; each would need individual approval per the updating-skills Iron Law
