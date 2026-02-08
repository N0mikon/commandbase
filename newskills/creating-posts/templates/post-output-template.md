# Post Output Template

Format templates for presenting generated posts and critique results to the user.

## Generate Mode Output

For each variant, present in this format:

```
### Variant [N]: [Angle] ([platform])

[char count]/[char limit] characters

` ` `
[The post text goes here — in a code fence for easy copying]
` ` `

Voice check: [PASS | N flagged items]
[If flagged: list specific issues]
```

Present 2-3 variants, then:

```
Want to use one of these, adjust one, or try different angles?
```

### Variant Angles

Label each variant with its approach:
- **Technical** — leads with the tech, how it works, trade-offs
- **Casual** — leads with the story, personal experience, conversational
- **Problem-focused** — leads with the pain point, why this exists

## Critique Mode Output

Present analysis in this format:

```
DRAFT REVIEW ([platform])
=========================

Tier 1 violations (must fix):
- "[flagged text]" — [why it's flagged] → [suggested replacement]
- "[flagged text]" — [why it's flagged] → [suggested replacement]

Tier 2 density: [count] flagged words ([threshold: max 2])
[If over threshold: list the words]

Tier 3 clustering: [PASS | flagged paragraphs]
[If flagged: identify which paragraphs have 3+ Tier 3 words]

Structural issues:
- Contractions: [present/missing]
- Voice: [active/passive clusters found]
- Sentence length: [varied/uniform]
- Parallel construction: [OK/overused]

Quick check:
1. Would you say this aloud to a colleague? [yes/no]
2. Does it include at least one specific example? [yes/no]
3. Is it jargon-free? [yes/no]

Suggested rewrite:
` ` `
[Full rewrite preserving core message, all issues fixed]
` ` `
[char count]/[char limit] characters
```

## Thread Output (Twitter/X Only)

For thread variants, present each tweet separately:

```
### Thread Variant [N]: [Angle]

**Tweet 1 (Hook):** [char count]/280
` ` `
[Hook tweet text]
` ` `

**Tweet 2:** [char count]/280
` ` `
[Detail tweet text]
` ` `

**Tweet 3:** [char count]/280
` ` `
[Detail tweet text]
` ` `

**Tweet [N] (CTA):** [char count]/280
` ` `
[CTA tweet text]
` ` `

Total: [N] tweets

Voice check: [PASS | N flagged items]
```
