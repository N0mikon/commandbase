# .docs/ Artifact Types Reference

Guide to `.docs/` artifact types, their expected content, and suggested vault placement.

## Artifact Type Overview

| Type | Directory | Purpose | Typical Size |
|------|-----------|---------|-------------|
| Research | `.docs/research/` | Investigation findings, analysis, evidence | Medium-large |
| Plan | `.docs/plans/` | Phased implementation plans with success criteria | Large |
| Design | `.docs/design/` | Architectural decisions, trade-offs, rationale | Medium |
| Structure | `.docs/structure/` | File/folder layout, module boundaries, placement rules | Medium |
| Handoff | `.docs/handoffs/` | Session continuity, progress state, next steps | Small-medium |
| Learning | `.docs/learnings/` | Lessons learned, patterns discovered, pitfalls | Small |
| Brainstorm | `.docs/brainstorm/` | Philosophy, preferences, direction exploration | Medium |
| Refactor | `.docs/refactors/` | Refactor scope, baseline state, migration plan | Medium |

## Per-Type Details

### Research (`.docs/research/`)

**Expected frontmatter:**
```yaml
date, status, topic, tags, git_commit, references
```

**Content patterns:**
- Question being investigated
- Findings organized by aspect/dimension
- Evidence with specific file/note references
- Summary and recommendations

**Vault placement suggestions:**
- Knowledge base folder (e.g., `Research/`, `References/`, `Projects/[name]/Research/`)
- Tag with research type and project name

**Conversion notes:**
- Code file references (`src/auth.ts:45`) may not be relevant in vault context — consider removing or keeping as inline code
- Evidence sections are the most valuable content for vault preservation

### Plan (`.docs/plans/`)

**Expected frontmatter:**
```yaml
date, status, topic, tags, git_commit, references
```

**Content patterns:**
- Overview and current state analysis
- Desired end state
- What we're NOT doing
- Phased implementation with success criteria
- Testing strategy

**Vault placement suggestions:**
- Projects folder (e.g., `Projects/[name]/Plans/`)
- Consider whether completed plans are worth importing (they may be historical)

**Conversion notes:**
- Checkboxes (`- [x]`) transfer directly
- Success criteria sections are useful for retrospectives
- Phase structure may be more detailed than vault notes typically need — consider summarizing
- Code-specific success criteria (test commands, type checks) may not be relevant

### Design (`.docs/design/`)

**Expected frontmatter:**
```yaml
date, status, topic, tags, git_commit, references
```

**Content patterns:**
- Design decisions organized by domain
- Trade-off analysis
- User preferences captured
- Claude's discretion decisions with rationale

**Vault placement suggestions:**
- Projects folder or Architecture folder
- Tag with design domains covered

**Conversion notes:**
- Decision tables and rationale are the most vault-worthy content
- "Claude's Discretion" sections document reasoning that's valuable for future reference

### Structure (`.docs/structure/`)

**Expected frontmatter:**
```yaml
date, status, topic, tags, git_commit, references
```

**Content patterns:**
- Directory/folder trees
- File/note placement rules
- Module/folder boundaries
- Migration sequencing

**Vault placement suggestions:**
- Projects folder or Architecture folder
- May overlap with design doc — consider merging

**Conversion notes:**
- Folder trees and placement rules are directly useful
- Migration steps may be outdated if already executed

### Handoff (`.docs/handoffs/`)

**Expected frontmatter:**
```yaml
date, status, topic, tags, session
```

**Content patterns:**
- What was done
- What's in progress
- Open questions
- Modified files list
- Next steps

**Vault placement suggestions:**
- Session logs folder (e.g., `Journal/Sessions/`, `Projects/[name]/Sessions/`)
- May not be worth importing unless the session had important insights

**Conversion notes:**
- Most ephemeral of all doc types — evaluate if content is still relevant
- Modified files list is code-specific and may not translate
- Open questions may be resolved — check before importing

### Learning (`.docs/learnings/`)

**Expected frontmatter:**
```yaml
date, status, topic, tags, source_session
```

**Content patterns:**
- Problem encountered
- Solution discovered
- Pattern to remember
- When to apply

**Vault placement suggestions:**
- Knowledge base folder (e.g., `Learnings/`, `Insights/`, `TIL/`)
- These are often the MOST valuable imports — direct knowledge capture

**Conversion notes:**
- Usually concise and vault-ready with minimal conversion
- Problem/solution format maps well to vault notes
- Consider linking to related project notes

### Brainstorm (`.docs/brainstorm/`)

**Expected frontmatter:**
```yaml
date, status, topic, tags, doc_type: brainstorm
```

**Content patterns:**
- Philosophy/preferences captured
- Deferred ideas
- Domain-specific decisions
- Next steps

**Vault placement suggestions:**
- Projects folder or Ideation folder
- Deferred ideas may warrant their own notes

**Conversion notes:**
- Philosophy decisions are valuable for vault context
- Deferred ideas should be converted to actionable notes or tasks
- "Next Steps" section may reference vault skills — translate to vault context

### Refactor (`.docs/refactors/`)

**Expected frontmatter:**
```yaml
date, status, topic, tags, git_commit, scope
```

**Content patterns:**
- Refactor scope and goals
- Baseline state
- Migration plan
- Risk assessment

**Vault placement suggestions:**
- Projects folder
- Usually code-specific — evaluate relevance before importing

**Conversion notes:**
- Code-specific refactor details may not translate to vault context
- Goals and lessons learned sections are most vault-worthy

## Batch Import Strategy

When importing multiple files:

1. **Group by type** — process all research docs together, then plans, etc.
2. **Establish convention mappings once** — frontmatter translation rules apply to all files of the same type
3. **Present summary table first** — show all source → target mappings before converting

```markdown
| Source | Type | Target | Status |
|--------|------|--------|--------|
| .docs/research/topic-a.md | Research | Research/topic-a | Ready |
| .docs/research/topic-b.md | Research | Research/topic-b | Ready |
| .docs/plans/feature-x.md | Plan | Projects/feature-x/plan | Ready |
| .docs/handoffs/session-1.md | Handoff | — | Skip (outdated) |
```

4. **Allow skipping** — not every artifact needs to be imported
5. **Process sequentially** — convert and confirm each file before moving to the next
