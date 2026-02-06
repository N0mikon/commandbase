# Web-Search-Researcher Agent vs /researching-codebases Skill

```yaml
git_commit: 46b48db
last_updated: 02-05-2026
topic: Comparison of web-search-researcher agent methodology vs researching-codebases skill methodology
tags: [agents, skills, methodology, research, web-search]
status: complete
references:
  - ~/.claude/agents/web-search-researcher.md
  - ~/.claude/skills/researching-codebases/SKILL.md
  - ~/.claude/skills/researching-codebases/reference/research-agents.md
  - ~/.claude/skills/researching-codebases/reference/evidence-requirements.md
```

## Research Question

How is the web-search-researcher agent better than simply saying "search the web for X"? How does its methodology compare to the /researching-codebases skill?

## Summary

The web-search-researcher agent embodies a **compressed version** of the same research philosophy as /researching-codebases, adapted for external web sources instead of local code. Both reject simple query-response patterns in favor of structured methodology with multiple search angles, source verification, and synthesized output. The key difference: /researching-codebases enforces its methodology through hard rules (Iron Law, Gate Function, evidence requirements), while web-search-researcher encodes methodology as behavioral guidance within a single agent prompt.

## Detailed Findings

### 1. What web-search-researcher adds over "search the web for X"

A bare "search the web for X" instruction gives Claude no methodology. The agent adds:

| Aspect | "Search the web for X" | web-search-researcher agent |
|--------|----------------------|----------------------------|
| **Search strategy** | Single query, hope for the best | 4-phase process: analyze query → strategic multi-angle search → fetch & evaluate → synthesize |
| **Query crafting** | Whatever the LLM generates | Identifies key terms, multiple search angles, broad-to-specific progression |
| **Source evaluation** | Takes first results | Prioritizes authoritative sources, notes dates/versions, flags conflicts |
| **Domain strategies** | Generic approach | Context-specific: API docs vs best practices vs troubleshooting vs comparisons each get different search patterns |
| **Efficiency** | May over-fetch or under-fetch | Starts with 2-3 searches, fetches 3-5 promising pages, refines iteratively |
| **Output structure** | Unstructured dump | Summary → detailed findings with attribution → additional resources → explicit gaps |
| **Search operators** | Rarely used | Mandates quotes, site: targeting, minus operators |

**Source:** `~/.claude/agents/web-search-researcher.md:12-106`

### 2. Shared Philosophy Between Both

Both the agent and the skill reject the same anti-pattern: **answering from surface-level investigation**.

| Principle | /researching-codebases | web-search-researcher |
|-----------|----------------------|----------------------|
| Don't answer from memory | "Don't answer from memory - spawn agents to verify" | Query analysis phase before any searching |
| Multiple angles | Minimum 2 parallel agents per question | Multiple search angles, broad-to-specific |
| Verify before synthesizing | Gate Function step 4: verify file:line references | Content fetching phase evaluates source quality |
| Structured output | Mandatory research document with template | Required output format with sections |
| Acknowledge gaps | Open Questions section in template | "Note gaps in available information" |
| Source attribution | Every claim needs file:line | Every finding needs source URL and quotes |

### 3. Key Differences in Enforcement

**/researching-codebases** uses **hard process gates**:
- Iron Law: "NO SYNTHESIS WITHOUT PARALLEL RESEARCH FIRST" - absolute rule
- Gate Function: 7 mandatory steps that cannot be skipped
- Red Flags table: explicit stop-conditions
- Rationalization Prevention: pre-answers common excuses for cutting corners
- Verification Checklist: checkboxes before writing the document
- Mandatory artifact: `.docs/research/MM-DD-YYYY-*.md` file every time

**web-search-researcher** uses **behavioral guidance**:
- Four-phase methodology described but not enforced by gates
- Quality attributes listed (accuracy, relevance, currency, authority, completeness, transparency)
- Search strategies described for different query types
- Output format specified but no enforcement mechanism
- No mandatory artifact creation
- No rationalization prevention

### 4. Architectural Difference

| Dimension | /researching-codebases | web-search-researcher |
|-----------|----------------------|----------------------|
| **Type** | Skill (orchestrator) | Agent (worker) |
| **Scope** | Orchestrates multiple sub-agents | Operates as a single agent |
| **Tools** | Spawns codebase-locator, codebase-analyzer, codebase-pattern-finder, docs-locator, docs-analyzer | Uses WebSearch, WebFetch, Read, Grep, Glob, LS directly |
| **Model** | Runs in main context (opus) | Runs on sonnet |
| **Parallelism** | Spawns 2+ parallel agents | Sequential search refinement within single agent |
| **Artifacts** | Always produces `.docs/research/` file | No persistent artifact |
| **Evidence standard** | file:line references, no guessing phrases | Source URLs with quotes |

### 5. What web-search-researcher Could Learn from /researching-codebases

The skill has several enforcement mechanisms the agent lacks:
- **Mandatory artifact creation** - research results persist across sessions
- **Rationalization prevention** - pre-answers excuses for cutting corners
- **Red flag detection** - explicit stop conditions when methodology is being violated
- **Verification checklist** - structured self-check before presenting results
- **Minimum agent count** - /researching-codebases requires minimum 2 parallel agents; web-search-researcher has no minimum search count

## Code References

- `~/.claude/agents/web-search-researcher.md` - Full agent definition (109 lines)
- `~/.claude/skills/researching-codebases/SKILL.md` - Main skill definition (196 lines)
- `~/.claude/skills/researching-codebases/reference/research-agents.md` - Available agents guide (71 lines)
- `~/.claude/skills/researching-codebases/reference/evidence-requirements.md` - Evidence standards (65 lines)
- `~/.claude/skills/researching-codebases/templates/research-document-template.md` - Output template (94 lines)

## Architecture Notes

The two components occupy different layers in the research stack:
- **web-search-researcher** is a leaf-level worker agent — it does the actual searching
- **/researching-codebases** is an orchestration layer — it decomposes questions, dispatches workers, and synthesizes

They could theoretically compose: /researching-codebases could spawn web-search-researcher as one of its parallel agents when a question requires both codebase analysis AND external context. Currently this doesn't happen because /researching-codebases only references codebase-* and docs-* agents.

## Open Questions

1. Should web-search-researcher adopt enforcement patterns (rationalization prevention, red flags) from /researching-codebases?
2. Should /researching-codebases be able to spawn web-search-researcher for questions that need external context?
3. Should web-search-researcher produce a persistent artifact (`.docs/research/` file) to prevent knowledge loss?
4. Is the single-agent architecture of web-search-researcher sufficient, or would a multi-agent web research orchestrator be more effective for complex questions?
