---
date: 2026-02-12
status: complete
topic: "CLAUDE.md Best Practices Deep Dive: Authoring, Optimization, and Knowledge Management Patterns"
tags: [research, claude-md, best-practices, obsidian, vault-management, token-optimization, progressive-disclosure]
git_commit: 9c4c7f4
---

# CLAUDE.md Best Practices Deep Dive: Authoring, Optimization, and Knowledge Management Patterns

## Research Question
What are the best practices for authoring, structuring, and optimizing CLAUDE.md files — particularly for Obsidian vault management and knowledge work contexts?

## Summary
This deep dive synthesizes findings from official Anthropic documentation, academic research (253 CLAUDE.md files analyzed), and community practitioners. The core tension is between comprehensiveness (more context = fewer iterations) and conciseness (bloated files degrade instruction-following uniformly). The resolution: progressive disclosure — lean root CLAUDE.md (~60-100 lines, <500 tokens) with modular @imports, path-specific rules in `.claude/rules/`, and domain knowledge offloaded to skills. For knowledge management vaults specifically, CLAUDE.md serves as a "vault constitution" defining structure, naming, frontmatter schema, linking conventions, and forbidden actions — while workflow-specific instructions live in skills loaded on-demand.

## Detailed Findings

### 1. The Size Optimization Question

**Official Anthropic Guidance** ([Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices)):
- "Keep it short and human-readable"
- "Less (instructions) is more"
- "For each line, ask: 'Would removing this cause Claude to make mistakes?' If not, cut it"
- "Bloated CLAUDE.md files cause Claude to ignore your actual instructions"

**Quantitative Benchmarks**:
- Community consensus: < 300 lines maximum, shorter is better
- HumanLayer's practice: root CLAUDE.md under 60 lines (~500 tokens)
- Frontier models follow ~150-200 instructions reliably; Claude Code's system prompt uses ~50, leaving ~100-150 for CLAUDE.md
- Instruction-following degrades linearly as instruction count increases
- 40k character threshold triggers performance warnings in Claude Code
- One user's file grew to 44.7k characters after 2 months of daily use — performance degraded significantly

**Sources:** [HumanLayer Blog](https://www.humanlayer.dev/blog/writing-a-good-claude-md), [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices), [GitHub Issue #2766](https://github.com/anthropics/claude-code/issues/2766)

### 2. The Grow vs. Shrink Debate

**Position A: Shrink (Majority View)**
- Move domain knowledge to skills (on-demand loading)
- Use progressive disclosure: tell Claude how to find information, not everything
- Keep CLAUDE.md for universal, broadly applicable rules only
- Rules enforceable by tools (ESLint, Prettier, TypeScript) should NOT be in CLAUDE.md

**Position B: Grow (Contrarian View)** ([Tyler Folkman](https://tylerfolkman.substack.com/p/stop-compressing-context)):
- Context collapse: 18,282 tokens compressed to 122 tokens dropped accuracy from 66.7% to 57.1%
- Stanford's ACE framework: 10.6% accuracy improvement with accumulation, 86.9% faster adaptation
- CLAUDE.md as "living playbook" with structured, itemized entries and unique identifiers

**Resolution**: The positions aren't contradictory — structured growth with unique identifiers (Folkman) while moving domain knowledge to skills (official). Accumulate high-signal entries, prune redundancy.

**Sources:** [Stop Compressing Context - Tyler Folkman](https://tylerfolkman.substack.com/p/stop-compressing-context), [Stop Bloating Your CLAUDE.md - alexop.dev](https://alexop.dev/posts/stop-bloating-your-claude-md-progressive-disclosure-ai-coding-tools/)

### 3. Progressive Disclosure Architecture

**Token Allocations** (recommended):
- Always-loaded (CLAUDE.md): ~500 tokens
- On-demand docs: ~200-500 tokens per file
- Domain agents: ~300-800 tokens per agent

**What NOT to include in CLAUDE.md**:
- Style rules (ESLint handles this)
- Formatting preferences (Prettier enforces it)
- Type guidance (TypeScript catches violations)
- Any rules automated tools already enforce

**What TO include**:
- Project overview and architecture
- Essential commands (that can't be inferred)
- Stack summary
- Pointers to specialized docs with explicit loading instructions
- Never rules (security, destructive actions)

**The "Further Reading" Pattern**:
```markdown
# Further Reading (read before tasks)
- `docs/vault-conventions.md`
- `docs/frontmatter-schema.md`
```
Directs Claude to fetch contextual knowledge rather than relying on training data.

**Sources:** [Stop Bloating Your CLAUDE.md - alexop.dev](https://alexop.dev/posts/stop-bloating-your-claude-md-progressive-disclosure-ai-coding-tools/), [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)

### 4. Hierarchical Memory System

**Memory Type Hierarchy** (most to least specific):

| Type | Location | Scope |
|------|----------|-------|
| Managed policy | `/Library/Application Support/ClaudeCode/CLAUDE.md` | Organization-wide |
| Project memory | `./CLAUDE.md` | Team-shared (source control) |
| Project rules | `./.claude/rules/*.md` | Modular, path-scoped |
| User memory | `~/.claude/CLAUDE.md` | Personal (all projects) |
| Local memory | `./CLAUDE.local.md` | Personal project-specific (gitignored) |
| Auto memory | `~/.claude/projects/<project>/memory/` | Claude's automatic notes |

More specific instructions take precedence over broader ones.

**Auto Memory** — Claude-written notes:
- First 200 lines of MEMORY.md loaded into system prompt every session
- Topic files loaded on-demand
- Separates human instructions (CLAUDE.md) from learned patterns (auto memory)
- Prevents CLAUDE.md bloat from accumulated observations

**Sources:** [Manage Claude's memory - Claude Code Docs](https://code.claude.com/docs/en/memory)

### 5. The @Import System: Critical Behavior

Files referenced with `@path/to/file.md` are **loaded immediately on launch**, NOT on-demand:
- Main CLAUDE.md read at session start
- All @referenced files loaded immediately
- All content combined into initial context
- Splitting into multiple files improves maintainability but doesn't reduce token consumption

**Lazy Loading Workaround**: Omitting the @ symbol results in lazy loading behavior — Claude loads parent file but referenced files load on-demand based on conversation context:
```markdown
## Changelogs
- Write for your audience: docs/changelog-conventions.md
```

**Feature request for lazy @imports was closed as NOT_PLANNED** ([GitHub #11759](https://github.com/anthropics/claude-code/issues/11759)).

**Sources:** [GitHub Issue #2766](https://github.com/anthropics/claude-code/issues/2766), [GitHub Issue #11759](https://github.com/anthropics/claude-code/issues/11759)

### 6. Path-Specific Rules with .claude/rules/

YAML frontmatter with `paths` field enables scoped rules:
```yaml
---
paths:
  - "daily-notes/**/*"
  - "templates/**/*"
---
# Daily Note Rules
- Use YYYY-MM-DD ddd format for filenames
- Include mood, energy, focus frontmatter fields
```

Rules files load with the same high priority as CLAUDE.md. Prevents priority saturation where monolithic files compete for attention.

**Sources:** [Claude Code Rules Directory - ClaudeFast](https://claudefa.st/blog/guide/mechanics/rules-directory)

### 7. Never Rules and Enforcement Patterns

**Common Vault Never Rules**:
- Never delete notes without explicit approval
- Never remove wiki-links during refactoring
- Never commit .env files or credentials
- Never use `git add -A` or `git add .`
- Always backup before bulk operations

**Emphasis techniques**: `**NEVER**`, `IMPORTANT:`, `YOU MUST` — increase odds Claude pays attention, but aren't foolproof in long conversations.

**Critical insight**: "If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise."

**Three-Layer Enforcement**:
1. CLAUDE.md instructions (probabilistic — LLM may ignore)
2. Hooks with exit code 2 (deterministic — blocks action)
3. Deny rules in settings.json (absolute — tool unavailable)

CLAUDE.md says "don't do X"; hooks enforce "you can't do X."

**Sources:** [Teaching Claude To Remember - Medium](https://medium.com/@porter.nicholas/teaching-claude-to-remember-part-1-lay-down-the-law-8bb7422ac31c), [Automate workflows with hooks - Claude Code Docs](https://code.claude.com/docs/en/hooks-guide)

### 8. Knowledge Management vs Code: Key Differences

**Code CLAUDE.md** typically includes:
- Tech stack and architecture
- Build/test commands
- Coding conventions
- Terminal command syntax

**Knowledge Vault CLAUDE.md** typically includes:
- Vault purpose and personal context
- Folder structure with explanations
- File naming conventions
- Tagging taxonomy rules
- Linking conventions (wikilinks, when to create new notes)
- Frontmatter schema (required/optional properties per note type)
- Tone preferences
- Forbidden actions

**Key difference**: Knowledge vaults need more "personality" context — how to write, what tone, what linking philosophy. Code projects need more "mechanics" context — how to build, test, deploy.

**Sources:** [Teaching Claude Code My Obsidian Vault](https://mauriciogomes.com/teaching-claude-code-my-obsidian-vault), [Using Claude Code with Obsidian](https://kyleygao.com/blog/2025/using-claude-code-with-obsidian/)

### 9. Real-World Knowledge Vault Implementations

**Knowledge Vault Pattern** ([GitHub Gist](https://gist.github.com/naushadzaman/164e85ec3557dc70392249e548b423e9)):
- Replaced Evernote, Notion, Asana, Otter.ai
- CLAUDE.md defines inbox processing workflow
- Status tags: `#status/to-evaluate` → `#status/evaluated` → `#status/adopted`
- "No more re-explaining context every session"

**PKM Starter Kit** ([obsidian-claude-pkm](https://github.com/ballred/obsidian-claude-pkm)):
- Goal-aligned cascading system (3-year vision → daily tasks)
- Custom agents: note-organizer, weekly-reviewer, goal-aligner, inbox-processor
- Git version control for automatic backups

**COG Second Brain** ([GitHub](https://github.com/huytieu/COG-second-brain)):
- 120+ braindumps processed, 95%+ source accuracy
- Evolution cycle: daily capture → weekly analysis → monthly synthesis

**Claude Diary** ([rlancemartin](https://rlancemartin.github.io/2025/12/01/claude_diary/)):
- `/diary` captures session details; `/reflect` analyzes patterns to update CLAUDE.md
- Updates target only `~/.claude/CLAUDE.md` with "one-line bullets"
- Author kept reflection manual — reviewing updates before they modify core instructions

**Sources:** Listed inline above

### 10. Iterative Teaching and Evolution

**The Teaching Loop** ([Mauricio Gomes](https://mauriciogomes.com/teaching-claude-code-my-obsidian-vault)):
- "When Claude makes a mistake, you teach it by adding a rule to the file, and it won't make that mistake again"
- Process: Ask → If wrong, correct once → Correction becomes rule in CLAUDE.md
- One user's CLAUDE.md grew from 3 lines to 370+ through this process

**Compartmentalized Instructions** ([Eleanor Konik](https://www.eleanorkonik.com/p/claude-obsidian-got-a-level-up)):
- "Long instruction files fail the same reason terms and conditions exist: they're technically correct and functionally ignored"
- Solution: Specific skills for specific actions. Small, focused instruction files loaded only when needed.

**Anti-Pattern**: Don't write theoretical concerns about what Claude might need. "Each addition should solve a real problem you have encountered."

**Pruning Rule**: "If Claude already does something correctly without the instruction, delete it."

**Sources:** Listed inline above

### 11. Empirical Analysis: 253 CLAUDE.md Files

**Research**: [On the Use of Agentic Coding Manifests](https://arxiv.org/html/2509.14744v1) (arXiv, September 2025)

**Structural findings**:
- Shallow hierarchies dominate: single H1 branching into median 5 H2 and 9 H3 headings
- Deep nesting rare: H4 in only 14.6% of files, H5 in just 2.0%
- Content categories by prevalence: Build/Run (77.1%), Implementation (71.9%), Architecture (64.8%), Testing (60.5%), Performance (12.7%), Security (8.7%)
- 15.4% explicitly define AI agent's role and responsibilities

**Implication**: Action-oriented, shallow structure is the proven pattern. Deep nesting is counterproductive.

### 12. Privacy and Safety Considerations

**Data leaves your machine** ([Eric Khun](https://erickhun.com/posts/partner-os-claude-mcp-obsidian/)):
- "Claude Code feels local, but files go to Anthropic's servers"
- Conscious directory exclusions needed
- Manual permission requests before file changes

**Cognitive outsourcing risks**:
- Thinking replacement vs enhancement
- Loss of natural filtering (human forgetting serves purposes)
- Echo chamber risk (AI amplifies biases)
- Core principle: "AI as a thinking partner, not a thinking replacement"

**Sources:** Listed inline above

## Source Conflicts

**Grow vs. Shrink**: Tyler Folkman advocates structured growth; official docs and most experts recommend minimal files. Resolution: structured growth with unique identifiers for high-signal entries, while domain knowledge moves to skills.

**Front-load vs. Progressive**: Some practitioners recommend front-loading comprehensive context to reduce iteration cycles; official guidance says minimize. Resolution: front-load for root CLAUDE.md within the ~500 token budget, use progressive disclosure for everything else.

**Emphasis effectiveness**: Some practitioners swear by `**NEVER**` and `IMPORTANT:`; others report these get ignored in long conversations. Resolution: emphasis helps for critical rules but isn't foolproof — use hooks for deterministic enforcement.

## Currency Assessment
- Most recent source: February 2026 (official Anthropic docs, Builder.io guide)
- Academic research: September 2025 (253-file empirical study)
- Topic velocity: Fast-moving (Claude Code updates monthly)
- Confidence in currency: High — official docs and active community consensus

## Open Questions
- What is the exact token threshold where instruction-following degradation becomes measurable?
- How does auto memory interact with CLAUDE.md for knowledge vault contexts specifically?
- What's the optimal ratio of CLAUDE.md rules to skills for a vault with 50+ conventions?
- How should multi-vault configurations handle shared vs vault-specific CLAUDE.md content?
- Does the lazy loading workaround (omitting @) reliably work across Claude Code versions?
