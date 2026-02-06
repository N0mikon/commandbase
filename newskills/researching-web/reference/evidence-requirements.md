# Evidence Requirements

Standards for web research findings and red flags to watch for.

## What Counts as Web Evidence

Research findings must include:

- Source URL for every claim
- Publication date or last-updated date when available
- Author or organization attribution
- Direct quotes for key claims (not paraphrased assumptions)
- Version numbers when discussing libraries or frameworks

## Source Quality Assessment

Evaluate each source on these dimensions:

| Dimension | Strong | Weak |
|-----------|--------|------|
| **Recency** | Published within 6 months | Over 1 year old with no updates |
| **Authority** | Official docs, core team, recognized expert | Anonymous blog, no credentials |
| **Specificity** | Covers the exact version/context asked about | Generic advice, wrong version |
| **Evidence** | Benchmarks, code examples, production data | Opinions without supporting data |
| **Consensus** | Multiple independent sources agree | Single source, no corroboration |

## Not Acceptable

These phrases indicate answering from training data, not research:

- "Based on my knowledge..."
- "Typically, frameworks like..."
- "Most developers prefer..."
- "It's generally considered..."
- "In my experience..."
- "The standard approach is..."

Every claim needs a URL from actual agent findings.

## Red Flags - STOP and Spawn Agents

If you notice any of these, STOP immediately:

- About to answer without spawning any web-search-researcher agents
- Using only training data without current web sources
- Providing recommendations without source URLs
- Citing a source without having fetched and verified it
- Synthesizing before all agents have returned
- Using a single search angle for a multi-faceted question
- About to write research document without agent results

**When you hit a red flag:**
1. Stop and acknowledge the shortcut
2. Spawn the appropriate agents
3. Wait for results
4. Only then continue

## Handling Conflicts Between Sources

When sources disagree:

1. **Note the conflict explicitly** - don't silently pick a side
2. **Check recency** - newer information often supersedes older
3. **Check authority** - official docs outweigh blog posts
4. **Check context** - sources may be correct for different situations
5. **Present both sides** with attribution and let the user decide

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I already know this topic well" | Your training data has a cutoff. Spawn agents. |
| "The web won't have better info" | You don't know that until you search. Search. |
| "One source is enough" | One source isn't research. Cross-reference. |
| "I can see the answer is obvious" | Obvious answers still need sourced verification. |
| "The user just needs a quick pointer" | Quick pointers with URLs are better than guesses. |
| "These search results are redundant" | Redundancy confirms consensus. That's valuable. |
| "I'll verify later" | Verify now. Later means never. |

## Verification Checklist

Before writing the research document:

- [ ] Spawned at least 2 web-search-researcher agents in parallel
- [ ] All agents returned results with source URLs
- [ ] Every finding has a URL attribution
- [ ] No "typically" or "generally" phrases without sources
- [ ] Cross-referenced findings between agents
- [ ] Flagged any conflicts between sources
- [ ] Noted source recency for time-sensitive topics
- [ ] Identified gaps or areas needing follow-up
