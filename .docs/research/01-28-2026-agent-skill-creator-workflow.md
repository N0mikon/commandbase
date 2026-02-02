---
git_commit: 448f0d24
last_updated: 2026-02-01
last_updated_by: docs-updater
last_updated_note: "Refreshed after 8 commits - external research, no content changes needed. Referenced by creating-skills-blueprint.md."
topic: "Agent Skill Creator - 6-Phase Autonomous Skill Creation Workflow"
tags: [research, skill-creator, agent-skill-creator, workflow, activation-system, meta-skill, FrancyJGLisboa, external-repo]
status: complete
references:
  - https://github.com/FrancyJGLisboa/agent-skill-creator
  - agent-skill-creator/SKILL.md
  - agent-skill-creator/.claude-plugin/marketplace.json
  - agent-skill-creator/references/phase1-discovery.md
  - agent-skill-creator/references/phase2-design.md
  - agent-skill-creator/references/phase3-architecture.md
  - agent-skill-creator/references/phase4-detection.md
  - agent-skill-creator/references/phase5-implementation.md
  - agent-skill-creator/references/phase6-testing.md
  - agent-skill-creator/references/quality-standards.md
  - agent-skill-creator/docs/NAMING_CONVENTIONS.md
  - agent-skill-creator/docs/CLAUDE_SKILLS_ARCHITECTURE.md
  - agent-skill-creator/docs/DECISION_LOGIC.md
  - agent-skill-creator/docs/INTERNAL_FLOW_ANALYSIS.md
  - agent-skill-creator/integrations/agentdb_bridge.py
  - agent-skill-creator/integrations/validation_system.py
  - agent-skill-creator/integrations/fallback_system.py
  - agent-skill-creator/integrations/learning_feedback.py
  - agent-skill-creator/scripts/export_utils.py
  - agent-skill-creator/article-to-prototype-cskill/
  - agent-skill-creator/references/examples/stock-analyzer-cskill/
---

# Research: Agent Skill Creator - 6-Phase Autonomous Skill Creation Workflow

**Date**: 2026-01-28
**Branch**: master
**Repo**: https://github.com/FrancyJGLisboa/agent-skill-creator
**Author**: FrancyJGLisboa
**Version**: 3.0.0 (Apache 2.0)

## Research Question

How does FrancyJGLisboa/agent-skill-creator implement its skill creator workflow? What is the 6-phase autonomous agent creation methodology, activation system, naming conventions, quality gates, and integration architecture?

## Summary

Agent Skill Creator is a **meta-skill** -- a Claude Code skill that autonomously creates other production-ready skills. It uses a 6-phase creation protocol (Discovery, Design, Architecture, Detection, Implementation, Testing), a 3/4-layer activation system for reliable skill triggering, the `-cskill` naming convention for generated skills, and an optional AgentDB integration for progressive learning. The repo contains ~93 files including the core SKILL.md (~107KB), a complete `/references` knowledge base (phase guides, quality standards, templates, tools), Python integration modules, and example generated skills.

## Repository Structure

```
agent-skill-creator/
├── .claude-plugin/
│   └── marketplace.json              # Plugin manifest (v3.0.0)
├── SKILL.md                          # Core meta-skill definition (~107KB)
├── README.md                         # User-facing docs (~2100 lines)
│
├── article-to-prototype-cskill/      # Example generated skill
│   ├── .claude-plugin/marketplace.json
│   ├── SKILL.md
│   ├── DECISIONS.md                  # 14 architectural decisions documented
│   ├── README.md
│   ├── references/                   # analysis-methodology, extraction-patterns, generation-rules
│   ├── scripts/
│   │   ├── analyzers/                # code_detector.py, content_analyzer.py
│   │   ├── extractors/              # markdown, notebook, pdf, web extractors
│   │   ├── generators/              # language_selector.py, prototype_generator.py
│   │   └── main.py
│   └── assets/                       # examples, prompts
│
├── docs/
│   ├── NAMING_CONVENTIONS.md         # The -cskill convention
│   ├── PIPELINE_ARCHITECTURE.md      # Pipeline skill patterns
│   ├── CLAUDE_SKILLS_ARCHITECTURE.md # Simple vs Complex vs Hybrid
│   ├── DECISION_LOGIC.md             # Architecture decision tree
│   ├── INTERNAL_FLOW_ANALYSIS.md     # End-to-end workflow trace
│   ├── AGENTDB_LEARNING_FLOW_EXPLAINED.md
│   ├── AGENTDB_VISUAL_GUIDE.md
│   ├── LEARNING_VERIFICATION_REPORT.md
│   ├── QUICK_VERIFICATION_GUIDE.md
│   ├── TRY_IT_YOURSELF.md
│   ├── USER_BENEFITS_GUIDE.md
│   ├── CHANGELOG.md
│   └── README.md
│
├── integrations/
│   ├── agentdb_bridge.py             # Invisible AgentDB integration layer
│   ├── agentdb_real_integration.py   # Real AgentDB CLI integration
│   ├── fallback_system.py            # Graceful degradation system
│   ├── learning_feedback.py          # Subtle learning progress indicators
│   └── validation_system.py          # Mathematical validation with proofs
│
├── references/                       # The "brain" - knowledge base
│   ├── phase1-discovery.md           # API research and selection
│   ├── phase2-design.md              # Analysis definition
│   ├── phase3-architecture.md        # Folder structure planning
│   ├── phase4-detection.md           # Activation system creation
│   ├── phase5-implementation.md      # Code generation
│   ├── phase6-testing.md             # Validation and QA
│   ├── quality-standards.md          # Mandatory quality gates
│   ├── activation-patterns-guide.md
│   ├── activation-quality-checklist.md
│   ├── activation-testing-guide.md
│   ├── context-aware-activation.md   # v3.1 Layer 4
│   ├── cross-platform-guide.md       # Desktop/Web/API compatibility
│   ├── export-guide.md
│   ├── multi-intent-detection.md
│   ├── synonym-expansion-system.md
│   ├── claude-llm-protocols-guide.md
│   ├── ACTIVATION_BEST_PRACTICES.md
│   ├── templates/
│   │   ├── marketplace-robust-template.json
│   │   └── README-activation-template.md
│   ├── tools/
│   │   ├── activation-tester.md
│   │   ├── intent-analyzer.md
│   │   └── test-automation-scripts.sh
│   └── examples/
│       └── stock-analyzer-cskill/    # Reference implementation
│           ├── .claude-plugin/marketplace.json
│           ├── SKILL.md
│           ├── README.md
│           ├── requirements.txt
│           └── scripts/main.py
│
├── exports/                          # Cross-platform export output
│   └── README.md
└── scripts/
    └── export_utils.py               # Cross-platform packaging utility
```

## Detailed Findings

### 1. Core Architecture: Meta-Skill Pattern

The repo is a **meta-skill** -- a SKILL.md that instructs Claude how to create other skills autonomously. The SKILL.md file (~107KB) contains the complete creation protocol, while the `/references` directory serves as the "brain" -- a knowledge base that guides each phase.

**SKILL.md frontmatter**:
```yaml
---
name: agent-skill-creator
description: This enhanced skill should be used when the user asks to create an agent,
  automate a repetitive workflow, create a custom skill, or needs advanced agent creation
  capabilities. Activates with phrases like every day, daily I have to, I need to repeat,
  create agent for, automate workflow, create skill for, need to automate, turn process
  into agent. Supports single agents, multi-agent suites, transcript processing,
  template-based creation, and interactive configuration.
---
```

**marketplace.json** (`.claude-plugin/marketplace.json`):
```json
{
  "name": "agent-skill-creator",
  "metadata": {
    "version": "3.0.0",
    "created": "2025-10-18",
    "updated": "2025-10-23",
    "features": ["multi-agent-support", "template-system", "transcript-processing",
                  "interactive-configuration", "batch-creation", "enhanced-validation"]
  },
  "plugins": [{
    "name": "agent-skill-creator-plugin",
    "description": "This enhanced meta skill should be used when...",
    "source": "./",
    "strict": false,
    "skills": ["./"]
  }],
  "activation": {
    "keywords": ["create an agent for", "create a skill for", "automate workflow",
                  "every day I have to", "daily I have to", "I need to repeat",
                  "need to automate", "turn process into agent",
                  "convert this transcript into agent", "convert this codebase into SKILL"],
    "patterns": [
      "(?i)(create|build|develop|make)\\s+(an?\\s+)?(agent|skill)\\s+(for|to|that)",
      "(?i)(automate|automation)\\s+(this\\s+)?(workflow|process|task|repetitive)",
      "(?i)(every day|daily|repeatedly)\\s+(I|we)\\s+(have to|need to|do|must)",
      "(?i)(turn|convert|transform)\\s+(this\\s+)?(process|workflow|task)\\s+into\\s+(an?\\s+)?agent",
      "(?i)need\\s+to\\s+automate",
      "(?i)(create|need)\\s+a\\s+custom\\s+skill",
      "(?i)I\\s+(repeatedly|constantly|always)\\s+(need to|have to|do)"
    ]
  }
}
```

Key enforcement: `plugins[0].description` MUST be identical to SKILL.md frontmatter description. This synchronization is enforced as Step 0 of Phase 5.

**Capabilities** (v3.0.0):
- Single agent creation (original)
- Multi-agent suite creation (v2.0)
- Transcript intelligence processing (v2.0)
- Template-based creation (v2.0) -- financial-analysis, climate-analysis, e-commerce-analytics
- Interactive configuration wizard (v2.0)
- Batch agent creation (v2.0)
- Cross-platform export (v3.2) -- Desktop, Web, API packages
- AgentDB intelligence integration (v2.1)

Installation: `/plugin marketplace add FrancyJGLisboa/agent-skill-creator`

### 2. The 6-Phase Autonomous Creation Protocol

The core workflow. Each phase has a dedicated reference guide in `/references/`.

#### Phase 1: DISCOVERY (API Research)
**Reference**: `references/phase1-discovery.md`

7-step process:
1. Identify domain from user input
2. Search available APIs with WebSearch
3. Research documentation with WebFetch
4. Create **API Capability Inventory** (mandatory: 70%+ coverage or explain why)
5. Compare 3+ options with weighted scoring:
   - Coverage: 30%
   - Cost: 20%
   - Rate limits: 15%
   - Quality: 15%
   - Documentation: 10%
   - Ease of use: 10%
6. DECIDE which API to use autonomously (with written justification)
7. Research technical details (authentication, endpoints, rate limits, quirks)

Also queries AgentDB (v2.1) for similar past successes to inform the decision. All decisions documented in DECISIONS.md.

#### Phase 2: DESIGN (Analysis Definition)
**Reference**: `references/phase2-design.md`

- Brainstorm 15-20 typical user questions for the domain
- Group by analysis type: simple queries, temporal comparisons, rankings, trends, projections, aggregations
- DEFINE 4-6 priority analyses covering 80% of use cases
- Specify each analysis: objective, inputs, outputs, methodology, formulas, validations, interpretation
- **MANDATORY**: Include `comprehensive_{domain}_report()` function combining ALL metrics into a single call

#### Phase 3: ARCHITECTURE (Structure Planning)
**Reference**: `references/phase3-architecture.md`

Architecture decision tree:

| Type | Criteria | LOC Range |
|------|----------|-----------|
| **Simple Skill** | Single objective, linear workflow | <1000 |
| **Complex Skill Suite** | Multiple objectives, multi-domain | >2000 |
| **Hybrid** | Core + optional extensions | 1000-2000 |

For each type:
- Define folder structure (scripts, utils, references, assets)
- Define per-script responsibilities (file name, function, input/output, estimated line count)
- Plan references (API guide, analysis methods, troubleshooting, domain knowledge)
- Performance strategy (cache TTL, rate limiting, parallelization, lazy loading)
- Apply `-cskill` naming convention
- Document architecture choice in DECISIONS.md with rationale

#### Phase 4: DETECTION (Activation System)
**Reference**: `references/phase4-detection.md`

**3-Layer System** (expanded to 4-Layer in v3.1):

| Layer | What | Target Count | Purpose |
|-------|------|-------------|---------|
| Layer 1 | Keywords | 50-80 phrases | Exact match activation |
| Layer 2 | Regex Patterns | 10-15 patterns | Flexible intent matching |
| Layer 3 | Description + NLU | 300-500 chars, 60+ keywords | Claude's natural language understanding |
| Layer 4 (v3.1) | Context-Aware Filtering | domain/task/intent analysis | False positive prevention |

**Keyword categories** (5 required):
1. Core capabilities
2. Synonym variations
3. Direct variations
4. Domain-specific
5. Natural language

**Entity categories**: Organizations/Sources, Main Objects, Geography, Metrics, Temporality
**Action categories**: Query, Compare, Analyze, Monitor, Transform

Also defines:
- `when_to_use` (5+ cases)
- `when_not_to_use` (3+ cases)
- `test_queries` (10+ queries covering all layers)
- Negative scope (what should NOT activate)

Target reliability: 95%+ (v2), 99.5% (v3.1)

#### Phase 5: IMPLEMENTATION (Code Generation)
**Reference**: `references/phase5-implementation.md`

Step-by-step order:
1. **Step 0 (MANDATORY)**: Create `.claude-plugin/marketplace.json` FIRST
   - Validate JSON syntax immediately
   - `plugins[0].description` MUST be identical to SKILL.md frontmatter description
2. Create directory structure
3. Create SKILL.md (5000-7000 words) with all mandatory sections
4. Implement Python scripts in order:
   - Utils first (helpers.py, cache_manager.py, rate_limiter.py, validators/)
   - Fetch (API client)
   - Parse (**MODULAR**: 1 parser per data type -- monolithic parsers explicitly forbidden)
   - Analyze (analysis functions + comprehensive_report)
5. Write references (1000-2000 words each, real content, no "see external docs")
6. Create assets (valid JSON with real values, not placeholders)
7. Write README.md and DECISIONS.md
8. Create VERSION and CHANGELOG.md

#### Phase 6: TESTING (Validation)
**Reference**: `references/phase6-testing.md`

Added as mandatory in v2.0:
- Generate test suite: test_fetch.py, test_parse.py, test_analyze.py, test_integration.py, test_validation.py, test_helpers.py, conftest.py
- One test function per `get_*()` method
- Integration tests with real API data
- Coverage target: 80%+
- ALL tests must PASS
- Test installation with `/plugin marketplace add ./agent-name`
- Minimum: 25+ tests

### 3. The `-cskill` Naming Convention

**Reference**: `docs/NAMING_CONVENTIONS.md`

**CSKILL** = **C**laude **SKILL** -- identifies skills autonomously created by Agent Skill Creator.

**Format**: `{descriptive-description}-cskill/`

**Rules**:
- Always lowercase
- Hyphens (-) as word separators only
- End with `-cskill`
- Alphanumeric + hyphens only (no underscores, spaces, special chars)
- No leading numbers
- Length: 10-60 characters (ideal: 20-40)
- No consecutive hyphens

**Name types**:

| Type | Pattern | Example |
|------|---------|---------|
| Simple | `{action}-{object}-cskill/` | `pdf-text-extractor-cskill/` |
| Suite | `{domain}-analysis-suite-cskill/` | `financial-analysis-suite-cskill/` |
| Component | `{functionality}-{domain}-cskill/` | `data-acquisition-cskill/` |

**Domain examples**:
- Finance: `portfolio-optimizer-cskill/`, `risk-calculator-cskill/`
- Data: `etl-pipeline-cskill/`, `dashboard-generator-cskill/`
- Documents: `pdf-processor-cskill/`, `excel-report-generator-cskill/`
- E-commerce: `inventory-tracker-cskill/`, `sales-analytics-cskill/`
- Research: `literature-review-cskill/`, `citation-manager-cskill/`

**Name generation logic**:
```python
def generate_skill_name(user_requirements, complexity):
    concepts = extract_key_concepts(user_requirements)
    if complexity == "simple":
        base_name = create_simple_name(concepts)
    elif complexity == "complex_suite":
        base_name = create_suite_name(concepts)
    base_name = sanitize_name(base_name)
    return f"{base_name}-cskill"

def validate_skill_name(skill_name):
    if not skill_name.endswith("-cskill"):
        return False, "Missing -cskill suffix"
    if skill_name != skill_name.lower():
        return False, "Must be lowercase"
    if not re.match(r'^[a-z0-9-]+-cskill$', skill_name):
        return False, "Contains invalid characters"
    if len(skill_name) < 10 or len(skill_name) > 60:
        return False, "Invalid length"
    if '--' in skill_name:
        return False, "Contains consecutive hyphens"
    return True, "Valid naming convention"
```

### 4. 3/4-Layer Activation System (Deep Dive)

The activation system is the most heavily documented component, with 7+ reference files dedicated to it.

**Layer 1 - Keywords** (`references/phase4-detection.md`):
- 50-80 complete phrases organized in 5 categories
- Target: 98% activation on exact matches

**Layer 2 - Regex Patterns** (`references/activation-patterns-guide.md`):
- 10-15 case-insensitive patterns using `(?i)` flag
- Cover verb/noun combinations with optional articles/prepositions
- Target: 98% activation on pattern matches

**Layer 3 - Description NLU** (`references/phase4-detection.md`):
- 150-250 character description packed with 60+ keywords
- Relies on Claude's natural language understanding
- Description in SKILL.md frontmatter AND marketplace.json MUST be identical

**Layer 4 - Context-Aware Filtering** (v3.1, `references/context-aware-activation.md`):
- Domain analysis, task analysis, intent analysis
- Negative filtering (exclude false positives)
- Relevance scoring with configurable thresholds
- Configured via `contextual_filters` in marketplace.json:
  ```json
  {
    "contextual_filters": {
      "required_context": [...],
      "excluded_context": [...],
      "context_weights": {...},
      "activation_rules": {...}
    }
  }
  ```

**Activation testing tools** (`references/tools/`):
- `activation-tester.md` -- Framework with Test Generator, Pattern Validator, Coverage Analyzer, Performance Monitor
- `test-automation-scripts.sh` -- Bash test suite generating 8 variations per keyword, combinatorial pattern tests, coverage calculator, HTML report generation
- `intent-analyzer.md` -- Multi-intent detection: primary + secondary intent parsing, compatibility analysis, execution order

**Reference implementation** (`references/examples/stock-analyzer-cskill/`):
- 65 keywords in 5 categories
- 12 regex patterns with detailed comments
- 80+ description keywords
- 46 test queries across all layers
- Results: Layer 1 100%, Layer 2 100%, Layer 3 90%, Integration 100%, Negative 100%, Overall 98%

**Synonym expansion system** (`references/synonym-expansion-system.md`):
- Systematic expansion from 10-15 base keywords to 50-80
- Category-based expansion (verbs, objects, connectors, domain terms)

### 5. Quality Standards

**Reference**: `references/quality-standards.md`

**Fundamental principles**:
- **Production-ready, not prototype** -- Code must work without modifications
- **Functional, not placeholder** -- No TODO, pass, NotImplementedError
- **Useful, not generic** -- Specific content, concrete examples

**Per-file requirements**:

| File Type | Requirements |
|-----------|-------------|
| **Python scripts** | Shebang, module docstring, organized imports, constants, type hints on all public functions, docstrings with Args/Returns/Raises/Example, try/except for risky operations, input/output validations, logging (info/debug/error), argparse main, `if __name__ == "__main__"` |
| **SKILL.md** | Valid frontmatter (name + 150-250 word description), 5000-7000 words, 9 mandatory sections: when to use, data source, workflows (step-by-step with commands), scripts explained, analyses documented, errors handled, validations listed, performance/cache, keywords/examples (5+) |
| **References** | 1000+ words, self-contained content, concrete examples with real values, executable code blocks, no "see documentation" links |
| **Assets/configs** | Syntactically valid JSON (python-validated), real values with instructions for user-configurable fields, inline comments via `_comment`/`_note` keys |
| **README** | Step-by-step installation, API key instructions, 5+ usage examples, specific troubleshooting |

**Anti-patterns explicitly forbidden**:
- Partial implementation
- Empty references ("see external docs")
- Useless configs with only placeholders ("YOUR_KEY_HERE" without instructions)
- TODO comments in production code
- `pass` or `NotImplementedError` in any function

### 6. AgentDB Integration Architecture

**Reference**: `integrations/`

Four Python modules form an invisible progressive learning layer:

**agentdb_bridge.py** -- Primary integration:
- `AgentDBBridge` class with silent auto-initialization
- `AgentDBIntelligence` dataclass: `template_choice`, `success_probability`, `learned_improvements`, `historical_context`, `mathematical_proof`
- `enhance_agent_creation()` -- Query for similar past successes, retrieve episodes, query causal effects
- `store_agent_experience()` -- Store reflexion data and causal relationships, extract skills
- Auto-detects CLI or npx availability, attempts automatic npm install
- 30-second timeout on all subprocess calls

**validation_system.py** -- Mathematical validation:
- `MathematicalValidationSystem` singleton via `get_validation_system()`
- Validates template selection (70% confidence threshold), API selection (60%), architecture (75%)
- SHA-256 Merkle proof hash generation for audit trail
- Falls back gracefully when AgentDB unavailable

**fallback_system.py** -- Graceful degradation:
- Modes: OFFLINE (cached data only), DEGRADED (basic features), SIMULATED (fake responses), RECOVERING
- Caches experiences when offline, syncs when online
- Domain-specific template fallbacks

**learning_feedback.py** -- Progress indicators:
- Subtle, non-intrusive feedback milestones
- Milestones: First success, Consistency (10 uses), Speed improvement (20%), Long-term usage (30 days)
- Pattern recognition: morning routines, Friday summaries, end-of-month reports
- Learning score: AgentDB (40%) + User engagement (30%) + Milestones (20%) + Consistency (10%)

**Key design principle**: **Zero-config, invisible intelligence**. Works perfectly without AgentDB installed, progressively enhances when available, never disrupts the user experience. Learning timeline:
- Day 1: Stores creation episodes
- After 10+ uses: 40% faster with learned patterns
- After 30+ days: Personalized recommendations

### 7. Cross-Platform Export

**Reference**: `scripts/export_utils.py`, `references/cross-platform-guide.md`

Packages created skills for multiple platforms:

| Platform | Format | Size Limit | Features |
|----------|--------|-----------|----------|
| Claude Code (CLI) | Git repo / plugin marketplace | None | Full support, git-based |
| Claude Desktop | .zip manual upload | ~10MB recommended | Full execution |
| claude.ai (Web) | .zip manual upload | ~10MB recommended | Same as Desktop |
| Claude API | Optimized .zip | 8MB hard limit | No network, no pip, sandboxed, max 8 skills/request |

Validation before export:
- SKILL.md exists with valid frontmatter
- Name <= 64 characters
- Description <= 1024 characters
- No `.env` or `credentials.json` files included
- Excludes `.git`, `__pycache__`, etc.

Auto-generates platform-specific installation guide.
Version detection: git tags > SKILL.md frontmatter > default `v1.0.0`.

### 8. Example Generated Skill: article-to-prototype-cskill

Complete example demonstrating the workflow output.

**Architecture**: Simple Skill (single objective, ~1800 LOC)

**Capability**: Extracts content from articles (PDF, web, notebooks, markdown) and generates prototype code in 5 languages (Python, JS/TS, Rust, Go, Julia).

**Pipeline**: Input > Extraction > Analysis > Language Selection > Generation > Output

**Language selection priority**: user hint > detected from code blocks > domain inference > dependency analysis > Python default

**DECISIONS.md** documents 14 architectural decisions with rationale:
1. Simple Skill architecture (single objective)
2. Multi-format extraction (specialized extractors per format with common interface)
3. Priority-based language selection
4. Template-based generation with quality gates (no TODOs)
5. Modular pipeline (Extract > Analyze > Select > Generate)
6. Rule-based content analysis (deterministic, no ML)
7. Dependency management (extract from imports + domain defaults)
8. Graceful degradation error handling
9. Generated test suite with placeholders
10. Multi-level caching (memory, disk 24h TTL, AgentDB persistent)
11. Auto-generated README with source attribution
12. 5 priority languages
13. AgentDB integration designed but optional
14. Language-specific project structure conventions

### 9. Marketplace Hierarchy

The repo defines a clear three-tier hierarchy:

```
Marketplace (container/registry)
  └── Plugin (executor, has marketplace.json)
       └── Skill(s) (functionality, each has SKILL.md)
            └── Components (scripts/, references/, assets/)
```

The marketplace.json structure enables:
- `activation.keywords` + `activation.patterns` for reliable triggering
- `usage.when_to_use` / `usage.when_not_to_use` for false positive prevention
- `usage.test_queries` for validation
- `capabilities` feature flags
- `contextual_filters` (v3.1) for context-aware activation

### 10. Internal Flow (End-to-End Trace)

**Reference**: `docs/INTERNAL_FLOW_ANALYSIS.md`

Walkthrough of user saying: "I'd like to automate what is being explained in this article [financial data analysis article]"

1. **Phase 0 - Detection**: Pattern matching on user input triggers the skill
2. **Phase 1 - Discovery**: Article content processing, API research via WebSearch/WebFetch, AgentDB enhancement, technology stack decision
3. **Phase 2 - Design**: Use case analysis, methodology definition
4. **Phase 3 - Architecture**: Complexity analysis against decision tree, component structure, performance planning
5. **Phase 4 - Detection**: Keyword analysis, description creation for the NEW skill being created
6. **Phase 5 - Implementation**: Directory creation, marketplace.json, SKILL.md per component, Python scripts, configs, references, README, installation test

Final output example: `financial-analysis-suite-cskill/` with:
- 4 component skills (data-acquisition, technical-analysis, visualization, reporting)
- Shared utils
- requirements.txt
- README.md + DECISIONS.md
- test_installation.py

## Architecture Notes

### Key Patterns

1. **Meta-skill pattern**: A skill whose purpose is creating other skills. SKILL.md contains the complete creation protocol; `/references` directory is the knowledge base guiding each phase.

2. **3/4-Layer activation system**: Keywords (exact) + Patterns (regex) + Description (NLU) + Context filtering. Target: 99.5% activation, <1% false positives.

3. **Autonomous decision-making**: Designed to minimize user questions. Researches APIs, selects architecture, defines analyses, implements code autonomously. Documents every decision in DECISIONS.md.

4. **Modular parser anti-pattern avoidance**: 1 parser per data type. Monolithic parsers explicitly forbidden.

5. **Mandatory comprehensive report**: Every created skill must include `comprehensive_{domain}_report()` combining all metrics.

6. **DECISIONS.md convention**: Every created skill documents all architectural choices with rationale, alternatives considered, and trade-offs.

7. **Invisible progressive learning**: AgentDB integration as transparent enhancement -- works without it, gets smarter with it, never disrupts.

8. **Marketplace.json synchronization**: `plugins[0].description` must be identical to SKILL.md frontmatter description. Enforced as Step 0.

9. **Synonym expansion**: Systematic keyword expansion from 10-15 base phrases to 50-80 via category-based expansion.

10. **Cross-platform packaging**: Single skill can be exported to CLI, Desktop, Web, and API formats with platform-specific optimizations.

### What Makes This Repo Distinct

Compared to other skill creators:

| Feature | Agent Skill Creator | Others |
|---------|-------------------|--------|
| **Phases** | 6 formal phases with dedicated reference guides | Typically 3-5 informal steps |
| **Activation** | 3/4-Layer system (keywords + regex + NLU + context) | Usually description-only |
| **Naming** | `-cskill` suffix convention | No standard convention |
| **Learning** | AgentDB progressive learning integration | No learning system |
| **Testing** | Mandatory 25+ tests, 80% coverage | Often no testing phase |
| **Export** | Cross-platform (CLI, Desktop, Web, API) | Usually CLI only |
| **Quality gates** | Explicit anti-patterns, per-file requirements | General guidelines |
| **Decision docs** | DECISIONS.md for every created skill | Not standard |
| **Autonomy** | Fully autonomous with justification | Usually interactive |
| **Templates** | Domain-specific (financial, climate, e-commerce) | Generic templates |

### Design Philosophy

- **Production-ready output**: No prototypes, no placeholders, no TODOs
- **Self-contained skills**: Each generated skill includes all references, configs, tests, and documentation
- **Predictable structure**: `-cskill` naming, consistent directory layout, documented decisions
- **Progressive enhancement**: Core workflow needs no external dependencies; AgentDB adds invisible intelligence over time
- **Autonomous operation**: Claude decides APIs, architectures, analyses without asking the user

## Code References

- Meta-skill definition: `SKILL.md` (root, ~107KB)
- Plugin manifest: `.claude-plugin/marketplace.json`
- Phase 1 guide: `references/phase1-discovery.md`
- Phase 2 guide: `references/phase2-design.md`
- Phase 3 guide: `references/phase3-architecture.md`
- Phase 4 guide: `references/phase4-detection.md`
- Phase 5 guide: `references/phase5-implementation.md`
- Phase 6 guide: `references/phase6-testing.md`
- Quality standards: `references/quality-standards.md`
- Activation patterns: `references/activation-patterns-guide.md`
- Activation checklist: `references/activation-quality-checklist.md`
- Activation testing: `references/activation-testing-guide.md`
- Context filtering: `references/context-aware-activation.md`
- Synonym expansion: `references/synonym-expansion-system.md`
- Multi-intent detection: `references/multi-intent-detection.md`
- Cross-platform guide: `references/cross-platform-guide.md`
- Export guide: `references/export-guide.md`
- Activation best practices: `references/ACTIVATION_BEST_PRACTICES.md`
- Claude LLM protocols: `references/claude-llm-protocols-guide.md`
- Marketplace template: `references/templates/marketplace-robust-template.json`
- README template: `references/templates/README-activation-template.md`
- Activation tester tool: `references/tools/activation-tester.md`
- Intent analyzer tool: `references/tools/intent-analyzer.md`
- Test automation scripts: `references/tools/test-automation-scripts.sh`
- Naming conventions: `docs/NAMING_CONVENTIONS.md`
- Architecture types: `docs/CLAUDE_SKILLS_ARCHITECTURE.md`
- Decision logic: `docs/DECISION_LOGIC.md`
- Internal flow trace: `docs/INTERNAL_FLOW_ANALYSIS.md`
- Pipeline architecture: `docs/PIPELINE_ARCHITECTURE.md`
- AgentDB bridge: `integrations/agentdb_bridge.py`
- Validation system: `integrations/validation_system.py`
- Fallback system: `integrations/fallback_system.py`
- Learning feedback: `integrations/learning_feedback.py`
- Export utility: `scripts/export_utils.py`
- Example skill: `article-to-prototype-cskill/`
- Reference skill: `references/examples/stock-analyzer-cskill/`

## Open Questions

1. The AgentDB integration references an external `agentdb` CLI tool -- its availability and current maintenance status are unclear
2. The SKILL.md is ~107KB which is unusually large for a skill file; whether this causes context window issues in practice is undocumented
3. The repo claims 94-97% time savings in README performance metrics but no independent benchmarks exist
4. The v3.1 4-Layer context-aware filtering is documented in references but its actual deployment status vs. aspirational is unclear
5. The `strict: false` setting in marketplace.json -- what does strict mode do and when would you enable it?
6. The export utility handles cross-platform packaging but there's no CI/CD integration for automated testing of exports
