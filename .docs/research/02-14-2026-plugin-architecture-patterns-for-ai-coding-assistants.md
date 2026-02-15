---
date: 2026-02-14
status: complete
topic: "Plugin Architecture Patterns for AI Coding Assistants"
tags: [research, plugin-architecture, skill-design, coverage-analysis, dependency-management]
git_commit: d53b95a
references:
  - .docs/learnings/02-12-2026-vault-skill-refinement-session-learnings.md
  - plugins/commandbase-meta/skills/creating-skills/SKILL.md
---

# Plugin Architecture Patterns for AI Coding Assistants

## Research Question
How should a "designing-plugins" skill codify patterns for: (1) organizing shared references across plugins, (2) deciding runtime vs knowledge dependencies, and (3) ensuring plugin suites cover both episodic and daily workflows?

## Summary
Research across AI coding assistant ecosystems (Claude Code, Cursor, Copilot, Aider) and mature plugin systems (VSCode, Obsidian, WordPress, Terraform) reveals three converging patterns: progressive disclosure for token efficiency, self-contained plugins with knowledge duplication preferred over runtime coupling, and a persistent blind spot where plugin suites optimize for episodic project workflows while neglecting daily habitual operations. No ecosystem formally distinguishes "knowledge dependencies" from "runtime dependencies," but the pattern exists implicitly across all mature systems.

## Detailed Findings

### 1. Shared Reference Organization Across Plugins

**Sources:** Claude Code docs (code.claude.com/docs/en/skills), Agent Skills spec (agentskills.io/specification), VSCode extension manifest docs, Terraform module best practices (developer.hashicorp.com)

**The convergence pattern:** All mature ecosystems use progressive disclosure — load metadata first, full content when triggered, detailed references on demand. Claude Code's three-tier model (100 tokens → 5000 tokens → full resources) is the most explicit implementation.

**Key finding: Split by use case, not by topic.** This was independently discovered during the vault-skill-refinement session (discovery 1) and is confirmed by Terraform's separation of providers (API interaction) from modules (reusable patterns). When multiple plugins need the same domain knowledge, each should get a reference file scoped to its consumption pattern.

**Cross-plugin reference sharing doesn't work at runtime.** No AI coding assistant ecosystem has a mechanism for one skill to reference another skill's files. Skills are self-contained units. The Agent Skills spec explicitly makes no provision for inter-skill dependencies. VSCode extensions can share APIs via `extensionDependencies` and exports, but even there, cross-host limitations break API sharing.

**Practical implication for commandbase:** Plugin-level `reference/` directories (like the new `commandbase-core/reference/batch-safety-protocol.md`) serve as design-time canonical sources. Skills in other plugins adapt these patterns into their own domain-specific reference files rather than pointing to them at runtime.

### 2. Runtime vs Knowledge Dependency Framework

**Sources:** Microservices shared library analysis (phauer.com, medium.com/@shanthi.shyju), WordPress plugin dependencies (WordPress 6.5 docs), Obsidian inter-plugin communication (forum.obsidian.md), Sam Newman's microservices guidance

**The core distinction (implicit across all ecosystems):**

| Dependency Type | Definition | Coupling | Update Impact | Example |
|-----------------|-----------|----------|---------------|---------|
| Runtime | Plugin needs another plugin's tools/hooks at execution time | Tight — both must be present | Breaking changes cascade | commandbase-code needs commandbase-core's docs-writer agent |
| Knowledge | Plugin uses another plugin's patterns at design time | None — baked in at creation | Source evolves independently | maintaining-vault adapts batch-safety-protocol from core |

**Sam Newman's principle applies directly:** "Don't violate DRY within a microservice, but feel free to violate DRY across microservices." Translated: don't duplicate within a skill, but duplicating reference patterns across plugins is acceptable and preferred over coupling.

**When runtime dependencies are acceptable:**
- Infrastructure/cross-cutting concerns (docs agents, error tracking hooks)
- Stable interfaces unlikely to change
- The dependency provides functionality, not just knowledge

**When knowledge duplication is preferred:**
- Domain-specific reference material (OFM syntax, safety protocols)
- Patterns that different consumers use differently
- Content that would bloat consumers with irrelevant material if shared as-is

**WordPress's cautionary tale:** Shared library dependency hell — multiple plugins bundling different versions of the same library creates conflicts based on unpredictable activation order. The proposed solution (namespace sandboxing) adds complexity. Better to avoid the problem entirely by preferring knowledge dependencies.

### 3. Coverage Gap Analysis: The Tuesday Test

**Sources:** Red Routes methodology (thedecisionlab.com), JTBD Big/Little Hire (Bob Moesta via intercom.com), DILO analysis (businessanalystmentor.com, mindtools.com), Task Analysis frequency matrix (userfocus.co.uk)

**No ecosystem has a formal gap analysis framework for plugin suites.** This is a genuine gap in the literature. However, four established UX/product frameworks combine into a practical approach:

**Framework 1: JTBD Big Hire / Little Hire**
- Big hire = when users adopt the tool (project setup, architecture decisions)
- Little hire = when users actually use it daily (quick capture, review, commit)
- "Real value is created in the little hire" — products that optimize for big hire but neglect little hire fail at retention

**Framework 2: Red Routes Matrix**
- Plot all skills on frequency (rarely → always) × user breadth (few → all)
- Red routes (high frequency, all users) = must-have daily operations
- One-off tasks (low frequency, high importance) = project setup workflows
- Gap appears when red routes have no skill coverage

**Framework 3: DILO (Day in the Life Of) Analysis**
- Map a typical development day chronologically
- For each time block, identify which skills would be invoked
- Uncovered time blocks = daily-use gaps
- This is essentially the "Tuesday test" formalized

**Framework 4: Task Analysis Frequency/Difficulty Matrix**
- High-frequency, difficult → redesign for efficiency (shortcuts, batch operations)
- High-frequency, easy → promote (make discoverable)
- Low-frequency, difficult → automate (wizards, step-by-step)
- Low-frequency, easy → keep as-is

**The synthesized "Tuesday Test" procedure:**
1. List all skills in the plugin suite
2. Classify each as episodic (project-level) or habitual (daily/weekly)
3. Walk through a typical day: "What does a user do with this tool on a normal Tuesday?"
4. For each daily activity, check if a skill covers it
5. Uncovered daily activities = gaps to fill
6. Verify the suite has at least one skill in each red route quadrant

**The vault-skill-refinement session validated this:** The original 8 vault skills covered setup and architecture (episodic) but zero daily operations. The Tuesday test revealed the gap, leading to 5 new daily-use skills (capturing, reviewing, connecting, maintaining, linting).

## Source Conflicts

**Progressive disclosure budgets:** Claude Code docs recommend SKILL.md under 500 lines / 5000 words. The Agent Skills spec says "under 5,000 tokens" for instructions. These aren't contradictory but use different units — the Claude Code guidance is more conservative.

**Dependency philosophy:** VSCode and WordPress formally support runtime dependencies. Obsidian and Aider do not. The microservices literature strongly favors avoiding shared dependencies. There's no consensus — the right choice depends on coupling tolerance and ecosystem maturity.

## Currency Assessment
- Most recent source: February 2026 (Agent Skills marketplace stats)
- Topic velocity: Fast-moving — Agent Skills spec launched Dec 2025, ecosystem growing rapidly
- Confidence in currency: High for architecture patterns, medium for ecosystem-specific details

## Open Questions
- Should commandbase formalize a "plugin design checklist" that includes the Tuesday test, or is this better as guidance in creating-skills?
- Is a standalone designing-plugins skill warranted, or do the patterns added to creating-skills (reference splitting, Tuesday test) plus this research document provide sufficient coverage?
- How should plugin-level reference files (like core's batch-safety-protocol.md) be versioned or updated when the canonical pattern evolves?
