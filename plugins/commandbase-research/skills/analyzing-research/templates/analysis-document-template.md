# Analysis Document Template

Use this template when writing cross-reference analysis findings to `.docs/research/`.

## File Naming

**Format:** `MM-DD-YYYY-analysis-<topic-slug>.md`

The `analysis-` prefix distinguishes synthesis documents from primary research.

**Examples:**
- `02-08-2026-analysis-skill-patterns.md`
- `02-08-2026-analysis-authentication-evolution.md`
- `02-10-2026-analysis-session-management-findings.md`

## Body Sections Template

Frontmatter is handled by the `docs-writer` agent. Provide these body sections as the `content` field:

```markdown
# Cross-Reference Analysis: [Topic]

**Date**: [Current date]
**Branch**: [Current git branch]
**Source documents**: [N] documents analyzed

## Analysis Scope
[What was cross-referenced and why — topic, tags, date range, or explicit file list]

## Source Documents

| # | Document | Date | Status | Commits Behind |
|---|----------|------|--------|----------------|
| 1 | [filename](relative-path) | YYYY-MM-DD | current/stale | 0/N |
| 2 | ... | ... | ... | ... |

## Shared Findings

Conclusions reinforced across multiple documents:

### [Finding Title]
**Cited in**: [doc1], [doc2], [doc3 if applicable]
[Description of the shared conclusion and what each document contributes to it]

### [Another Finding]
...

## Contradictions

Places where documents disagree:

### [Contradiction Topic]
- **[doc1]** concludes: [position A]
- **[doc2]** concludes: [position B]
- **More recent**: [which document]
- **Assessment**: [which is likely more accurate and why, or "needs re-research"]

*If no contradictions found, state: "No contradictions detected across source documents."*

## Temporal Evolution

How understanding changed over time:

### [Topic That Evolved]
- **[earliest date]** ([doc]): [initial understanding]
- **[later date]** ([doc]): [revised understanding]
- **[latest date]** ([doc]): [current understanding]
- **Trend**: [what direction the understanding is moving]

*If documents don't cover overlapping topics over time, state: "Source documents cover distinct topics — no temporal evolution detected."*

## Gaps Resolved

Open questions from one document answered by another:

### [Question from doc1]
- **Asked in**: [doc1] (Open Questions section)
- **Answered in**: [doc2]
- **Resolution**: [the answer found]

*If no gaps were resolved, state: "No cross-document gap resolutions found."*

## Emergent Patterns

Patterns visible only when comparing across documents:

### [Pattern Name]
**Observed in**: [doc1], [doc2], [doc3]
[Description of the pattern and why it matters — this is the insight no single document could provide]

## Remaining Questions

Questions still open after cross-referencing:
- [Question not answered by any source document]
- [New question raised by the cross-referencing itself]
```

## Section Guidelines

### Source Documents
- List every document included in the analysis
- Include staleness data so readers know confidence levels
- Sort by date (oldest first) to show chronological progression

### Shared Findings
- Only include findings cited in 2+ documents
- Explain what each document contributes — don't just say "both agree"
- 3-7 findings is typical; more than 10 suggests the documents are too similar

### Contradictions
- State both positions neutrally before assessing
- Recency matters but isn't the only factor — a thorough old analysis may be more accurate than a hasty new one
- If a contradiction can't be resolved, recommend re-research

### Temporal Evolution
- Only include topics that genuinely changed over time
- Don't force evolution where documents simply cover different subtopics
- Note whether changes represent genuine learning or just different scope

### Gaps Resolved
- Only count genuine matches: the open question and the answer must be about the same thing
- Note partial resolutions honestly

### Emergent Patterns
- This is the highest-value section — insights impossible from any single document
- Each pattern must cite 3+ documents to distinguish it from coincidence
- Patterns can be thematic (same concern keeps appearing), structural (same approach keeps being chosen), or temporal (same direction of change)

### Remaining Questions
- Include questions from source documents that weren't resolved
- Add new questions that emerged from the cross-referencing
- These are candidates for future `/researching-code` or `/researching-web` invocations
