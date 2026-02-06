# Web Research Document Template

Use this template when writing web research findings to `.docs/research/`.

## File Naming

**Format:** `MM-DD-YYYY-description.md`

- MM-DD-YYYY is today's date
- description is a brief kebab-case description of the topic

**Examples:**
- `02-05-2026-nextjs-auth-libraries.md`
- `02-05-2026-bun-vs-deno-comparison.md`
- `02-05-2026-react-server-components-best-practices.md`

## Template

```markdown
# [Research Topic]

## Metadata

```yaml
date_searched: MM-DD-YYYY
topic: "[Research Topic]"
tags: [web-research, relevant-topic-tags]
status: complete
query_decomposition:
  - "[Search angle 1 description]"
  - "[Search angle 2 description]"
  - "[Search angle 3 description]"
sources:
  - url: "[URL]"
    title: "[Page title]"
    date: "[Publication date if known]"
    authority: "[official/expert/community/individual]"
  - url: "[URL]"
    title: "[Page title]"
    date: "[Publication date if known]"
    authority: "[official/expert/community/individual]"
```

## Research Question

[Original user query]

## Summary

[2-4 sentences answering the question directly, citing the most authoritative sources]

## Detailed Findings

### [Topic/Angle 1]

**Sources:** [URL1], [URL2]

[Findings from this search angle with direct quotes and attributions]

### [Topic/Angle 2]

**Sources:** [URL1], [URL2]

[Findings from this search angle]

### [Topic/Angle 3]
...

## Source Conflicts

[Document any disagreements between sources. If none, state "No conflicts found - sources are consistent."]

- **[Topic of disagreement]**: [Source A] says X, while [Source B] says Y.
  - Likely explanation: [version difference, context difference, outdated info]
  - Recommendation: [which to trust and why]

## Currency Assessment

[How current are these findings?]

- Most recent source: [date]
- Oldest source: [date]
- Topic velocity: [fast-moving/stable] - [how quickly does this information change?]
- Confidence in currency: [high/medium/low]

## Open Questions

[Areas that need further investigation]
```

## Section Guidelines

### Summary
- 2-4 sentences answering the research question directly
- Cite the most authoritative source
- State the consensus view clearly
- Note if there is no consensus

### Detailed Findings
- One subsection per search angle
- Each finding needs a source URL
- Include direct quotes for key claims
- Note publication dates for time-sensitive information

### Source Conflicts
- Always include this section, even if just to say "no conflicts"
- When conflicts exist, explain the likely reason
- Note which source to trust and why (recency, authority, specificity)

### Currency Assessment
- Required for any technology-related research
- Fast-moving topics (JS frameworks, AI tools): findings may be stale within months
- Stable topics (algorithms, protocols): findings remain valid longer
- Be explicit about the shelf life of these findings

### Open Questions
- Areas where no authoritative source was found
- Follow-up questions that emerged during research
- Topics that would benefit from deeper investigation
