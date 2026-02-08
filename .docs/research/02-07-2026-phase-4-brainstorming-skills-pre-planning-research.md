---
date: 2026-02-07
status: complete
topic: "Phase 4 Brainstorming Skills - Pre-Planning Research"
tags: [research, brainstorming, phase-4, brdspi, discussing-features, retirement]
git_commit: 0713c81
references:
  - ".docs/plans/02-07-2026-future-skills-implementation-roadmap.md"
  - ".docs/future-skills/brainstorming.md"
  - "~/.claude/skills/discussing-features/SKILL.md"
  - "~/.claude/skills/designing-code/SKILL.md"
  - "~/.claude/skills/structuring-code/SKILL.md"
  - "~/.claude/skills/starting-refactors/SKILL.md"
  - "~/.claude/skills/starting-projects/SKILL.md"
  - "~/.claude/skills/creating-skills/SKILL.md"
  - "~/.claude/agents/docs-writer.md"
---

# Phase 4 Brainstorming Skills - Pre-Planning Research

**Date**: 2026-02-07
**Branch**: master

## Research Question

What does the current skill ecosystem look like, what patterns exist, and what decisions have already been made — so that a Phase 4 implementation plan can be written with full context for building three brainstorming skills and retiring `/discussing-features`?

## Summary

Phase 4 adds three domain-specific brainstorming skills (`/brainstorming-code`, `/brainstorming-vault`, `/brainstorming-services`) that replace the generic `/discussing-features` skill. The brainstorming skills sit at position zero in the BRDSPI chain — before any initializer or RDSPI phase — and produce `.docs/brainstorm/` artifacts that capture direction and preferences for downstream phases. The `/discussing-features` skill's domain detection system, 4-question rhythm, and preference questioning patterns must be absorbed into `/brainstorming-code`, while research-informed technical choices were already absorbed by `/designing-code` in Phase 2. The `docs-writer` agent needs a 9th doc_type (`brainstorm`) added, and the `.docs/brainstorm/` output directory does not yet exist.

## Scope: 5 Work Items

| Item | Type | Complexity | Key Challenge |
|------|------|-----------|---------------|
| `/brainstorming-code` | New skill | Low-Medium | Absorbing `/discussing-features` domain detection + adding codebase-aware exploration |
| `/brainstorming-vault` | New skill | Low-Medium | Vault-specific question domains without Vault BRDSPI built yet |
| `/brainstorming-services` | New skill | Low-Medium | Infrastructure-specific question domains without Services BRDSPI built yet |
| Retire `/discussing-features` | Archive | Low | Clean removal after absorption confirmed |
| Extend `docs-writer` agent | Modification | Low | Add `brainstorm` doc_type (3-line change following Phase 2 pattern) |

## Detailed Findings

### 1. Design Decisions Already Made

These decisions are settled in the roadmap and should NOT be re-debated during planning:

- **Naming convention**: All three skills follow `brainstorming-{domain}` gerund-form kebab-case (roadmap:294-322)
- **Output directory**: `.docs/brainstorm/` artifacts, not `.docs/context/` (roadmap:304,312,320)
- **Workflow position**: Always first step, before any initializer or RDSPI phase (future-skills/brainstorming.md:24-32)
- **`/discussing-features` retirement**: Archive after `/brainstorming-code` absorbs its content (roadmap:324-330)
- **Absorption split**: Domain detection + preference questions → `/brainstorming-code`; research-informed technical choices → already in `/designing-code` (roadmap:326-328)
- **Each skill produces artifacts**: Decision was "yes" — brainstorming produces `.docs/brainstorm/` files, not just conversational (roadmap:304,312,320; resolves open question from future-skills/brainstorming.md:36)

### 2. `/discussing-features` — Complete Functionality to Absorb

The skill being retired (188 lines + 2 supporting files) provides these capabilities:

#### 2a. Domain Detection System (discussing-features/SKILL.md:62-79)

Five domain types detected by analyzing feature descriptions for action verbs:

| If users will... | Domain | Example Topics |
|------------------|--------|----------------|
| SEE it | visual | Layout, density, interactions, empty states |
| CALL it | api | Response format, errors, versioning, auth |
| RUN it | cli | Flags, output format, progress, error handling |
| READ it | content | Structure, tone, depth, navigation |
| ORGANIZE with it | system/organization | Criteria, grouping, naming, exceptions |

Detection process: (1) Analyze feature description for action verbs, (2) Identify primary user interaction mode, (3) If mixed: identify DOMINANT mode, secondary informs sub-questions.

**Absorption target**: `/brainstorming-code` inherits this system but expands it with codebase-aware exploration (pattern/API/data model questions that `/discussing-features` couldn't ask).

#### 2b. 4-Question Rhythm (discussing-features/SKILL.md:96-111)

Interaction pattern per discussion topic:
1. Announce: "Let's talk about [Topic]"
2. Ask 4 questions using `AskUserQuestion` with 2-3 concrete options + "You decide" + automatic "Other"
3. After 4 questions: "More questions about [topic], or move on?"
4. If "More" → 4 more questions; if "Move on" → next topic

Design principles: Options are concrete ("Cards" not "Option A"), each answer can inform the next question, "Other" captures free-form input.

**Absorption target**: All three brainstorming skills inherit this rhythm pattern.

#### 2c. Topic Selection (discussing-features/SKILL.md:83-93)

Present 3-4 domain-specific topics using `AskUserQuestion` with `multiSelect: true`. Critical rule: NO "skip all" option — user invoked this command to discuss, give them concrete topics.

**Absorption target**: All three brainstorming skills inherit topic selection.

#### 2d. Scope Guardrail (discussing-features/SKILL.md:113-123)

Template response for out-of-scope mentions:
```
"[Mentioned capability] sounds like it belongs in a separate feature.
I'll note it as a deferred idea so it's not lost.
Back to [current topic]: [return to current question]"
```
Deferred ideas tracked for inclusion in output artifact.

**Absorption target**: All three brainstorming skills inherit scope guardrail.

#### 2e. Output Artifact — `.docs/context/` with XML Tags (discussing-features/templates/context-template.md)

Current output structure:
```yaml
---
feature: "[Feature Name]"
domain: [visual|api|cli|content|organization]
gathered: [YYYY-MM-DD]
status: ready-for-planning
---
```
Body sections with XML tags (`<domain>`, `<decisions>`, `<specifics>`, `<deferred>`) for downstream parsing by `/researching-code` and `/planning-code`.

**Key decision for Phase 4**: Brainstorming skills will produce `.docs/brainstorm/` artifacts instead of `.docs/context/`. The output format needs redesigning — the XML tags were consumed by `/researching-code` and `/planning-code`, but the brainstorming flow now goes through `/designing-code` first (which reads `.docs/research/` and `.docs/context/`, not `.docs/brainstorm/`). The new artifact format must be consumable by the correct downstream skills.

#### 2f. Supporting Files

- `reference/question-domains.md` (151 lines): Complete question templates for all 5 domains with example questions, trigger keywords, mixed domain handling, and boundary rules (DON'T ask / DO ask)
- `templates/context-template.md` (93 lines): Output template with XML tags, quality checklist

### 3. BRDSPI Core Interface Points — What Brainstorming Must Flow Into

#### 3a. `/designing-code` Input Requirements (designing-code/SKILL.md:44-60)

**Mandatory**: Research artifacts from `.docs/research/` — hard gate redirects to research skills if missing.
**Optional**: Feature context from `.docs/context/`.
**Optional**: Refactor scope from `.docs/refactors/`.

`/designing-code` does NOT read from `.docs/brainstorm/`. This means brainstorming skills need to either:
- Option A: Produce artifacts that `/designing-code` already knows how to read (`.docs/context/` or `.docs/research/`)
- Option B: Modify `/designing-code` to also check `.docs/brainstorm/`
- Option C: Accept that brainstorming → research → design is the intended flow, and brainstorming artifacts inform the human, not the downstream skill directly

**Recommendation**: Option C aligns with the roadmap's stated flow: "Flows into `/starting-projects` or `/starting-refactors` → R → D → S → P → I" (roadmap:305). Brainstorming captures direction and preferences that the user carries forward; the research phase then investigates within those constraints.

#### 3b. `/starting-projects` Input Requirements (starting-projects/SKILL.md:42-48)

**No upstream artifacts consumed** — this skill initiates the greenfield path via interactive discovery questions. Brainstorming output would inform the user's answers to discovery questions, not be consumed programmatically.

#### 3c. `/starting-refactors` Input Requirements (starting-refactors/SKILL.md:46-58)

**From user**: Target area, refactor goal, trigger reason. No BRDSPI artifacts consumed — this skill initiates the refactor chain. Same pattern as `/starting-projects`.

#### 3d. Artifact Chain Pattern

The full BRDSPI chain produces artifacts in a relay:
```
/brainstorming-* → .docs/brainstorm/ (direction + preferences — human-consumed)
     ↓ (user carries context forward)
/starting-* → .docs/refactors/ or .docs/plans/project-setup.md
     ↓
/researching-* → .docs/research/
     ↓
/designing-code → .docs/design/
     ↓
/structuring-code → .docs/structure/
     ↓
/planning-code → .docs/plans/
     ↓
/implementing-plans → code changes + checkpoints
```

Brainstorm artifacts are primarily human-consumed. They capture "what direction are we going?" and "what does the user prefer?" so the user can make informed choices in subsequent phases. They are NOT programmatically parsed by downstream skills (unlike `.docs/context/` which used XML tags).

### 4. Existing Skill Structural Patterns

All skills follow a consistent 11-section template. Brainstorming skills must follow this pattern:

| Section | Pattern | Required |
|---------|---------|----------|
| Frontmatter | `name:` + `description:` (WHEN formula) | Yes |
| Title + Role | H1 + "You are tasked with..." | Yes |
| Iron Law | Code-fenced absolute rule + "No exceptions" list | Yes |
| Gate Function | Numbered checklist, "BEFORE [action]", ends with "Skipping steps = [consequence]" | Yes |
| Initial Response | Conditional: if args provided vs no args | Yes |
| Process Steps | Numbered workflow with concrete instructions | Yes |
| Important Guidelines | Numbered behavioral principles | Yes |
| Red Flags | "STOP and Verify" bullet list | Yes |
| Rationalization Prevention | Excuse vs Reality table | Yes |
| The Bottom Line | Bold statement + "This is non-negotiable. Every [X]. Every time." | Yes |
| Example Interaction | Code-fenced user/assistant dialog | Optional |

#### Line Count Targets (from existing research-phase skills)

| Skill | SKILL.md Lines | Reference Files | Templates |
|-------|---------------|-----------------|-----------|
| `/researching-code` | ~233 | 2 (research-agents.md, evidence-requirements.md) | 1 (research-document-template.md) |
| `/researching-web` | ~268 | 2 (search-strategies.md, evidence-requirements.md) | 1 (web-research-document-template.md) |
| `/researching-repo` | ~223 | 2 (clone-management.md, analysis-strategies.md) | 1 (repo-research-template.md) |
| `/discussing-features` | 188 | 1 (question-domains.md) | 1 (context-template.md) |

**Target for brainstorming skills**: ~180-220 lines for SKILL.md, 1 reference file (question domains), 1 template (brainstorm output).

### 5. `/brainstorming-code` — Detailed Design Analysis

This is the most complex of the three because it absorbs `/discussing-features` functionality.

#### What it absorbs from `/discussing-features`:
- Domain detection system (5 domains: visual, api, cli, content, organization)
- 4-question rhythm with concrete options
- Topic selection with `multiSelect: true`
- Scope guardrail with deferred idea tracking
- Quality checklist for output artifacts

#### What it adds beyond `/discussing-features`:
- **Codebase-aware exploration**: Can reference existing patterns, APIs, data models (roadmap:300)
- **Direction choices**: Higher-level than preference questions — "REST or GraphQL?", "monolith or microservices?" (roadmap:302)
- **Flow into initializers**: Explicitly suggests `/starting-projects` or `/starting-refactors` as next step (roadmap:305)

#### Reference file structure:
- `reference/question-domains.md` — Adapted from `/discussing-features` version (151 lines → ~160-180 lines with codebase-specific additions)
- Can reuse most of the existing domain definitions, trigger keywords, and example questions
- Add code-specific exploration questions: "What patterns does the existing codebase use?", "Event-driven or polling?", "Monorepo or polyrepo?"

#### Template file structure:
- `templates/brainstorm-template.md` — New output format for `.docs/brainstorm/` artifacts
- Simpler than `/discussing-features`' context template — no XML tags needed since downstream consumption is human-mediated
- Should include: direction decisions, preference captures, deferred ideas, suggested next steps

### 6. `/brainstorming-vault` — Design Analysis

Vault-specific exploration that stands alone even before Phase 6 (Vault BRDSPI) is built.

#### Domain-specific questions (from roadmap:308-312):
- Structure: "Flat tags or nested folders?", "One MOC or topic hubs?"
- Linking: "Wikilinks or markdown links?", "Backlinks or forward links?"
- Templates: "Templater or manual?", "Daily notes or weekly?"
- Organization: "PARA or Zettelkasten or hybrid?"

#### Reference file:
- `reference/vault-question-domains.md` — Vault-specific question templates (~100-120 lines)
- Cannot reuse `/discussing-features`' domain detection — vault has its own domains (structure, linking, templates, organization, plugins)

#### Template file:
- Shares the same `templates/brainstorm-template.md` pattern as `/brainstorming-code` (or uses a shared template via symlink/copy)
- Output goes to `.docs/brainstorm/` with vault-specific frontmatter fields

#### Flow consideration:
- Currently flows into Vault BRDSPI (Phase 6, not yet built)
- Should still be useful standalone for vault planning conversations
- Next step suggestion: "When Vault BRDSPI is available: `/starting-vault`. For now: use these decisions to guide vault work manually."

### 7. `/brainstorming-services` — Design Analysis

Infrastructure exploration for homelab/Docker service management.

#### Domain-specific questions (from roadmap:316-320):
- Stack: "Authelia or Cloudflare tunnels?", "Traefik or Nginx Proxy Manager?"
- Compose: "Single compose or per-service?", "Shared network or isolated?"
- Backup: "Borg or restic?", "Local or remote or both?"
- Dependencies: "Which services depend on which?", "Startup order matters?"

#### Reference file:
- `reference/services-question-domains.md` — Infrastructure-specific question templates (~100-120 lines)
- Completely different domain knowledge from code or vault

#### Template file:
- Shares the same brainstorm template pattern
- Output goes to `.docs/brainstorm/` with services-specific frontmatter fields

#### Flow consideration:
- Currently flows into Services BRDSPI (Phase 7, not yet built)
- Same standalone usefulness pattern as vault
- Next step suggestion: "When Services BRDSPI is available: `/researching-services`. For now: use these decisions to guide infrastructure work manually."

### 8. `docs-writer` Agent Extension

The `docs-writer` agent (at `~/.claude/agents/docs-writer.md`) currently supports 8 doc_types. Adding `brainstorm` requires:

| Change | Location | Detail |
|--------|----------|--------|
| Add to enum | Line 32 area | Add `brainstorm` to valid types list |
| Update count | Line 44 area | Change "8 valid types" to "9 valid types" |
| Add mapping | Lines 63-72 area | Add row: `brainstorm` → `.docs/brainstorm/` → `draft` |

This is a 3-line change following the exact pattern used in Phase 2 when `design`, `structure`, and `refactor` doc_types were added.

### 9. Brainstorm Output Template Design

The brainstorm output artifact needs a new template since `.docs/context/` with XML tags is being replaced.

#### Proposed template structure:
```markdown
---
topic: "[Brainstorm Topic]"
domain: [code|vault|services]
date: [YYYY-MM-DD]
status: draft
---

# [Topic] - Brainstorm

## Direction
[High-level direction settled during brainstorming — 2-3 sentences]

## Decisions
### [Topic 1]
- [Specific preference or direction choice]

### [Topic 2]
- [Specific preference or direction choice]

### Claude's Discretion
[Areas where user said "you decide" — or "User provided specific preferences for all topics."]

## Deferred Ideas
[Ideas that came up but belong elsewhere — or "None"]

## Next Steps
[Suggested next skill invocation with rationale]
```

#### Key differences from `/discussing-features` context template:
- No XML tags (downstream consumption is human-mediated, not programmatic)
- `domain` field uses `code|vault|services` instead of `visual|api|cli|content|organization`
- Simpler frontmatter (no `feature` field, uses `topic` instead)
- Explicit "Next Steps" section guiding user to appropriate initializer or research skill

### 10. Proposed Skill File Structures

#### `/brainstorming-code` (most complex — absorbs `/discussing-features`)
```
brainstorming-code/
├── SKILL.md              (~200-220 lines)
├── reference/
│   └── question-domains.md  (~160-180 lines, adapted from discussing-features)
└── templates/
    └── brainstorm-template.md  (~60-70 lines)
```
**Total: 3 files, ~420-470 lines**

#### `/brainstorming-vault`
```
brainstorming-vault/
├── SKILL.md              (~180-200 lines)
├── reference/
│   └── vault-question-domains.md  (~100-120 lines)
└── templates/
    └── brainstorm-template.md  (~60-70 lines, same structure as code version)
```
**Total: 3 files, ~340-390 lines**

#### `/brainstorming-services`
```
brainstorming-services/
├── SKILL.md              (~180-200 lines)
├── reference/
│   └── services-question-domains.md  (~100-120 lines)
└── templates/
    └── brainstorm-template.md  (~60-70 lines, same structure as code version)
```
**Total: 3 files, ~340-390 lines**

### 11. Workflow Integration

#### Position in BRDSPI chain:
```
/brainstorming-*    ← Phase 0: explore direction, capture preferences
     ↓
/starting-*         ← Initialize workspace (greenfield or refactor)
     ↓
/researching-*      ← Investigate within brainstorming constraints
     ↓
/designing-code     ← Make architectural decisions
     ↓
/structuring-code   ← Map file placement
     ↓
/planning-code      ← Task breakdown
     ↓
/implementing-plans ← Execute with checkpoints
```

#### Brainstorming is optional:
- For lightweight features: skip directly to research or planning
- For greenfield projects: brainstorm → `/starting-projects` → RDSPI
- For refactors: brainstorm → `/starting-refactors` → RDSPI
- The BRDSPI chain works with or without brainstorming (backward compatible)

#### Cross-domain flow:
- `/brainstorming-code` → `/starting-projects` or `/starting-refactors` → code RDSPI
- `/brainstorming-vault` → Vault BRDSPI (Phase 6, not yet built)
- `/brainstorming-services` → Services BRDSPI (Phase 7, not yet built)

### 12. `/discussing-features` Retirement Plan

#### What was already absorbed by Phase 2:
- Research-informed technical choices → `/designing-code` (roadmap:328)
- Technical architecture questions → `/designing-code` design domains (designing-code/reference/design-domains.md)

#### What Phase 4 must absorb:
- Domain detection system (5 types) → `/brainstorming-code` (expanded with codebase exploration)
- 4-question rhythm → all three brainstorming skills
- Topic selection with `multiSelect: true` → all three brainstorming skills
- Scope guardrail + deferred idea tracking → all three brainstorming skills
- Question boundary rules (DON'T ask / DO ask) → adapted per domain

#### Retirement process:
1. Deploy `/brainstorming-code` and verify it covers all `/discussing-features` functionality
2. Remove `/discussing-features` from `~/.claude/skills/` (deployed)
3. Keep `/discussing-features` in `newskills/` as archive reference (roadmap:329)
4. Update any cross-references in other skills that mention `/discussing-features`

#### Skills that reference `/discussing-features`:
- Roadmap references it in Phase 0, Phase 4 (will be updated as part of implementation)
- No deployed skills currently invoke or depend on `/discussing-features` programmatically
- `/designing-code` absorbed the research-informed technical choices but doesn't reference `/discussing-features` by name

## Code References

- `~/.claude/skills/discussing-features/SKILL.md:1-188` — Full skill definition being retired
- `~/.claude/skills/discussing-features/reference/question-domains.md:1-151` — Domain detection + question templates
- `~/.claude/skills/discussing-features/templates/context-template.md:1-93` — Output template with XML tags
- `~/.claude/skills/designing-code/SKILL.md:44-60` — Input requirements (reads .docs/research/ and .docs/context/)
- `~/.claude/skills/designing-code/SKILL.md:83-102` — Design domain categorization
- `~/.claude/skills/structuring-code/SKILL.md:44-63` — Input requirements (reads .docs/design/)
- `~/.claude/skills/starting-refactors/SKILL.md:46-58` — Input requirements (user-provided)
- `~/.claude/skills/starting-projects/SKILL.md:42-48` — Input requirements (interactive discovery)
- `~/.claude/skills/creating-skills/SKILL.md:28-48` — Gate function for skill creation
- `~/.claude/skills/creating-skills/templates/workflow-skill-template.md:1-177` — Workflow skill template
- `~/.claude/agents/docs-writer.md:32,44,63-72` — Doc_type configuration (8 types, needs 9th)
- `.docs/future-skills/brainstorming.md:1-39` — Original brainstorming concept
- `.docs/plans/02-07-2026-future-skills-implementation-roadmap.md:292-337` — Phase 4 specification

## Architecture Notes

### Pattern: Human-Mediated Artifact Chain
Brainstorming artifacts are consumed by humans, not by downstream skills. This differs from the research → design → structure → plan chain where each skill programmatically reads the previous phase's output. The brainstorming output informs the user's decision-making when they invoke the next skill, rather than being parsed by that skill directly. This is intentional — brainstorming is exploratory and its output constrains the human's choices, not the tool's behavior.

### Pattern: Domain-Specific Question Banks
Each brainstorming skill has its own question domain reference file because the domains are fundamentally different. Code has visual/api/cli/content/organization domains. Vault has structure/linking/templates/organization/plugins domains. Services has stack/compose/backup/dependencies domains. Sharing a single question bank would force artificial abstraction.

### Pattern: Shared Interaction Rhythm, Separate Content
The 4-question rhythm, topic selection via `multiSelect`, scope guardrail, and deferred idea tracking are universal patterns shared across all three brainstorming skills. The content (specific questions, domain detection triggers, example options) is domain-specific. This suggests the SKILL.md files will share structural sections (Iron Law, Gate Function, process flow) but differ in domain references.

### Pattern: Graceful Degradation for Incomplete Chains
`/brainstorming-vault` and `/brainstorming-services` must work standalone even though their full BRDSPI chains (Phases 6 and 7) don't exist yet. The "Next Steps" section should detect whether the downstream chain exists and suggest manual workflow if it doesn't.

## Open Questions

1. **Shared brainstorm template or per-domain templates?** All three skills produce `.docs/brainstorm/` artifacts with similar structure. Should they share one template file (copied to each skill) or have domain-specific variations? The `domain` frontmatter field differs but body structure is identical.

2. **Should `/brainstorming-code` spawn codebase research agents?** The roadmap says it explores "patterns, APIs, data models, existing codebase conventions" (roadmap:300). Should it spawn `code-analyzer`/`code-locator` agents for lightweight exploration, or should full codebase research remain exclusively in `/researching-code`? Lightweight exploration would add value but blurs the brainstorm/research boundary.

3. **Does `/designing-code` need modification to read `.docs/brainstorm/`?** Currently it reads `.docs/research/` (mandatory) and `.docs/context/` (optional). The brainstorming output replaces `.docs/context/`. Should `/designing-code` be updated to also check `.docs/brainstorm/`, or is the human-mediated flow sufficient?

4. **Question domain overlap between `/brainstorming-code` and `/designing-code`?** Both ask users about API design, error handling, and architecture. The intended split is: brainstorming asks direction questions ("REST or GraphQL?") while design asks informed-by-research questions ("given our findings, JWT or session auth?"). How strictly should this boundary be enforced in the question banks?

5. **What happens to `.docs/context/` directory?** `/discussing-features` produced `.docs/context/` artifacts. After retirement, should existing context files be migrated, archived, or left in place? No deployed skills currently consume `.docs/context/` programmatically (only `/discussing-features` created them).

6. **Should the `/brainstorming-code` description mention `/discussing-features` retirement?** The skill description triggers Claude's invocation. Should it include phrases like "replaces /discussing-features" or "for feature discussions" to catch users who habitually invoke the old skill name?
