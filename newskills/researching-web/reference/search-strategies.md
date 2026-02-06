# Search Strategies

Guide to crafting effective search prompts for web-search-researcher agents by domain.

## Decomposition Patterns

Every research question should be broken into 2-4 distinct search angles. These patterns show how to decompose common question types.

### API/Library Documentation

```
Angle 1: "[library] official documentation [feature]"
Angle 2: "[library] changelog [version] breaking changes"
Angle 3: "[library] [feature] examples tutorial"
```

**Agent prompt template:**
```
Search for [library name] official documentation on [feature].
Focus on the official docs site and GitHub repository.
Include version-specific details for [version].
Note any recent changes in changelogs or migration guides.
```

### Best Practices

```
Angle 1: "[topic] best practices [year]" from recognized experts
Angle 2: "[topic] anti-patterns common mistakes"
Angle 3: "[topic] production experience lessons learned"
```

**Agent prompt template:**
```
Search for [topic] best practices published in [year range].
Prioritize content from recognized experts and organizations.
Cross-reference multiple sources to identify consensus.
Include both recommended practices and common anti-patterns.
```

### Library/Framework Comparisons

```
Angle 1: "[X] vs [Y]" direct comparison articles
Angle 2: "[X] to [Y] migration guide" transition experiences
Angle 3: "[X] [Y] benchmarks performance" quantitative data
```

**Agent prompt template:**
```
Search for "[X] vs [Y]" comparisons published in [year range].
Find benchmark data, migration guides, and developer experience reports.
Look for decision matrices or evaluation criteria.
Note the context of each recommendation (project size, team, use case).
```

### Troubleshooting/Error Resolution

```
Angle 1: "[exact error message]" solutions
Angle 2: "[technology] [error type] GitHub issues"
Angle 3: "[technology] [error context] workaround"
```

**Agent prompt template:**
```
Search for solutions to this error: "[exact error message]".
Check Stack Overflow, GitHub issues for [repository], and technical forums.
Look for both root cause explanations and working workarounds.
Note which versions are affected and whether fixes exist in newer releases.
```

### Architecture/Design Decisions

```
Angle 1: "[pattern] architecture [technology]" reference implementations
Angle 2: "[pattern] vs [alternative] tradeoffs"
Angle 3: "[technology] [pattern] production scale experience"
```

**Agent prompt template:**
```
Search for [architecture pattern] implementations in [technology].
Find real-world case studies and experience reports.
Look for tradeoff analysis between [pattern] and [alternative approaches].
Prioritize content from teams that have run this in production.
```

## Search Operator Guidance

Instruct agents to use these operators for precision:

| Operator | Purpose | Example |
|----------|---------|---------|
| `"quoted phrase"` | Exact match | `"useEffect cleanup"` |
| `site:` | Target specific domain | `site:docs.stripe.com webhooks` |
| `-` | Exclude terms | `Next.js auth -NextAuth` (to find alternatives) |
| `after:` | Recent results | `Bun test runner after:2025` |
| `OR` | Multiple terms | `"Clerk" OR "Auth0" Next.js comparison` |

## Source Authority Tiers

When instructing agents, guide them toward higher-authority sources:

| Tier | Source Type | Examples |
|------|-----------|----------|
| **1 - Official** | Documentation, specs, release notes | docs.stripe.com, react.dev, RFC documents |
| **2 - Recognized expert** | Known authors, core team members | Dan Abramov on React, Evan You on Vue |
| **3 - Community consensus** | High-vote answers, popular articles | Stack Overflow accepted answers, widely-shared posts |
| **4 - Individual experience** | Blog posts, tutorials, case studies | Personal blogs, Medium articles |

Agents should search across tiers but weight findings accordingly.

## Agent Count Guidelines

| Question Complexity | Agents | Reasoning |
|-------------------|--------|-----------|
| Factual lookup ("what is the API for X?") | 2 | Official docs + community examples |
| Comparison ("X vs Y") | 3 | Direct comparison + each option's strengths |
| Best practices ("how should I do X?") | 3 | Official guidance + expert consensus + anti-patterns |
| Architecture decision | 3-4 | Pattern docs + alternatives + production experiences + tradeoffs |

Never fewer than 2. The minimum ensures at least two search angles.
