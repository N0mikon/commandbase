---
name: analyzing-research
description: "Use this skill when cross-referencing multiple research documents to find patterns, contradictions, or emergent insights. This includes synthesizing findings across .docs/ files, comparing conclusions from different research sessions, detecting how understanding evolved over time, identifying gaps where one document's open questions were answered by another, and drawing higher-order conclusions not visible in any single document. Trigger phrases: '/analyzing-research', 'cross-reference research', 'compare these research files', 'what patterns across research', 'synthesize findings', 'connect the dots'."
---

# Analyzing Research

You are tasked with reading multiple `.docs/` documents, extracting their core findings, and synthesizing cross-document insights that no individual document contains on its own.

**Violating the letter of these rules is violating the spirit of these rules.**

## Your Role

Find what individual research missed by connecting it:
- Identify shared conclusions reinforced across documents
- Surface contradictions between documents
- Track how understanding evolved over time
- Match open questions in one document with answers in another
- Detect emergent patterns only visible when documents are compared
- Do NOT re-research the original topics — work with what the documents contain
- Do NOT critique document quality — synthesize their content

## The Iron Law

```
NO CONCLUSIONS WITHOUT MULTI-DOCUMENT EVIDENCE
```

Every cross-reference insight must cite at least two source documents. If a finding comes from only one document, it belongs in that document's summary, not in your synthesis.

**No exceptions:**
- Don't draw conclusions from a single document — that's summarizing, not analyzing
- Don't invent connections that aren't supported by the text
- Don't skip the extraction phase and synthesize from memory
- Don't present single-document findings as cross-document insights

## The Gate Function

```
BEFORE synthesizing:

1. DISCOVER: Find relevant documents (docs-locator or user-provided paths)
2. VERIFY MINIMUM: At least 3 documents required for meaningful cross-referencing
   - If fewer than 3: Tell user, suggest running more research first
3. CHECK FRESHNESS: Read frontmatter git_commit for each document
   - Note commits behind HEAD — flag stale documents in output
   - Include stale documents but mark them clearly
4. EXTRACT: Spawn parallel docs-analyzer agents (batch 3-5 docs per agent)
5. WAIT: All agents must complete before proceeding
6. SYNTHESIZE: Compare extracted insights across documents
7. WRITE: Create .docs/research/MM-DD-YYYY-analysis-<topic>.md (MANDATORY)
8. PRESENT: Summary to user with link to analysis file

Skip any step = superficial analysis that misses the cross-document value
```

## Initial Response

When invoked:

1. **If specific files or a topic were provided**, begin analysis immediately
2. **If no parameters provided**, respond with:
```
I'm ready to analyze across your research documents. Tell me what to cross-reference:

- A topic: "analyze research about skills" (I'll find relevant docs)
- Specific files: "analyze these 3 files: ..."
- A tag: "analyze everything tagged 'authentication'"
- A time range: "analyze research from the last week"
- Full sweep: "analyze all research documents"
```

Then wait for the user's input.

## Input Detection

Determine the discovery mode from the user's input:

| Input Type | Example | Discovery Method |
|-----------|---------|-----------------|
| **Topic** | "analyze research about auth" | Spawn `docs-locator` with topic keywords |
| **Explicit files** | "analyze these files: path1, path2" | Read file list directly |
| **Tag** | "analyze everything tagged 'skills'" | Grep frontmatter for tag matches |
| **Temporal** | "analyze research from last week" | Glob `.docs/` then filter by frontmatter date |
| **Full sweep** | "analyze all research" | Glob `.docs/research/**/*.md` |
| **Cross-type** | "connect research and learnings about X" | Spawn `docs-locator` across directories |

**Scope expansion**: By default, search `.docs/research/`. When the user's query implies broader scope (mentions plans, learnings, handoffs, or uses terms like "everything about X"), extend search to additional `.docs/` subdirectories. Use frontmatter tags and topic to decide relevance — don't pull in documents just because they exist in a directory.

## Process

### Step 1: Discover Documents

**For topic/tag/temporal/full sweep modes**, spawn a `docs-locator` agent:

```
Task prompt (docs-locator):
  Search .docs/ for documents related to [topic/tag/date range].
  Check: .docs/research/, .docs/plans/, .docs/learnings/, .docs/handoffs/
  [Only expand beyond .docs/research/ if user's query warrants it]
  Return: file paths, frontmatter dates, tags, and status for each match.
```

**For explicit file mode**, skip this step — read the paths directly.

After discovery, present the document set:

```
Found [N] documents to cross-reference:

1. [path] (date, [N] commits behind)
2. [path] (date, current)
3. [path] (date, [N] commits behind — flagged stale)
...

Proceeding with analysis.
```

If fewer than 3 documents found, stop:
```
Only [N] document(s) found. Cross-referencing needs at least 3 documents
to produce meaningful synthesis. Consider running more research first:
- /researching-code for codebase questions
- /researching-web for external topics
```

### Step 2: Check Freshness

For each document, check staleness via git:

```bash
commit=$(head -10 "$f" | grep "^git_commit:" | awk '{print $2}')
if [ -n "$commit" ] && [ "$commit" != "n/a" ]; then
  git rev-parse "$commit" >/dev/null 2>&1 && \
  behind=$(git rev-list "$commit"..HEAD --count 2>/dev/null)
fi
```

Record commits-behind for each document. Documents are included regardless of staleness but flagged in the output.

### Step 3: Extract Insights

Spawn parallel `docs-analyzer` agents, batching 3-5 documents per agent:

```
Task prompt (docs-analyzer):
  Read and extract key insights from these documents:
  1. [path1]
  2. [path2]
  3. [path3]

  For EACH document, return:
  - Document path and date
  - Key decisions made
  - Core findings and conclusions
  - Constraints or limitations identified
  - Open questions listed
  - File/code references mentioned
  - Tags from frontmatter

  Focus on extractable FACTS and DECISIONS, not summaries.
  Return structured output per document.
```

Wait for ALL agents to complete before proceeding.

### Step 4: Synthesize Cross-Document Insights

With all extracted insights in context, perform these five analyses:

**4a. Shared Findings**
Identify conclusions that appear in 2+ documents. These are reinforced insights — higher confidence because independently discovered.

**4b. Contradictions**
Find places where documents disagree or present conflicting conclusions. Note which documents conflict, what each says, and which is more recent.

**4c. Temporal Evolution**
When documents cover the same topic at different dates, trace how understanding changed. What was believed first? What was revised? What was abandoned?

**4d. Gap Resolution**
Match open questions from one document against findings in another. If Document A asks "how does X work?" and Document B answers it, that's a resolved gap.

**4e. Emergent Patterns**
Identify patterns visible only when comparing across documents — recurring themes, consistent constraints, architectural trends, repeated decisions.

### Step 5: Write Analysis Document

Spawn a `docs-writer` agent via the Task tool:

```
Task prompt (docs-writer):
  doc_type: "research"
  topic: "analysis-<topic slug>"
  tags: [analysis, cross-reference, <topic-specific tags>]
  references: [<all source document paths>]
  content: |
    <compiled analysis using the template from ./templates/analysis-document-template.md>
```

See ./templates/analysis-document-template.md for the output format.

### Step 6: Present Findings

Present a concise summary structured as:

```
## Cross-Reference Analysis: [Topic]

**Source documents**: [N] documents spanning [date range]
**Stale documents**: [N] flagged ([list])

### Key Insights
- [Top 3-5 cross-document findings, each citing 2+ source docs]

### Contradictions Found
- [Any conflicts between documents, or "None detected"]

### Gaps Resolved
- [Open questions from one doc answered by another, or "None found"]

Full analysis: .docs/research/MM-DD-YYYY-analysis-<topic>.md

Follow-up options:
- Re-research stale documents with /researching-code or /researching-web
- Dig deeper into a specific finding
- Analyze a different document set
```

## Important Guidelines

1. **Synthesize, Don't Summarize**
   - Individual summaries belong in the source documents
   - Your value is the CONNECTIONS between documents
   - Every insight must cite 2+ documents

2. **Respect the Evidence**
   - Don't extrapolate beyond what documents actually say
   - Flag low-confidence connections clearly
   - Note when stale documents may contain outdated conclusions

3. **Attribution Is Mandatory**
   - Every finding cites its source document(s)
   - Format: `(source: [filename], [filename])`
   - Contradictions cite both sides

4. **Preserve Nuance**
   - Don't flatten contradictions into false consensus
   - Note partial overlaps honestly
   - Distinguish "same conclusion" from "similar conclusion"

## Red Flags - STOP and Reconsider

If you notice any of these, pause:

- Drawing conclusions from a single document (that's summarizing)
- Presenting analysis without creating a file first
- Skipping the extraction phase and working from memory
- Forcing connections that aren't supported by document text
- Analyzing fewer than 3 documents without telling the user
- Making changes or recommendations beyond what was asked (scope creep)

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Two documents is enough" | Three is the minimum. Two is comparison, not cross-referencing. |
| "I already know what these documents say" | Spawn docs-analyzer anyway. Memory is unreliable. |
| "This finding is obviously connected" | Show the evidence from 2+ documents. Nothing is obvious. |
| "The stale documents aren't worth including" | Include them flagged. Staleness is context, not disqualification. |
| "The output doesn't need a file" | Every analysis produces a file. No exceptions. |
| "I'll just summarize each document" | Summaries aren't analysis. Find the CONNECTIONS. |

## The Bottom Line

**No cross-document conclusions without multi-document evidence.**

Discover the documents. Extract with agents. Synthesize the connections. Write the file. THEN present findings.

This is non-negotiable. Every analysis. Every time.
