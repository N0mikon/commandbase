---
git_commit: 8e92bba
last_updated: 2026-01-28
last_updated_by: rcode agent
topic: "Anthropic Skills Repository - Official Skill Creator & Reference Skills"
tags: [research, skills, skill-creator, anthropic, agent-skills, packaging, validation]
status: complete
references:
  - skills/skill-creator/SKILL.md
  - skills/skill-creator/scripts/init_skill.py
  - skills/skill-creator/scripts/package_skill.py
  - skills/skill-creator/scripts/quick_validate.py
  - skills/skill-creator/references/output-patterns.md
  - skills/skill-creator/references/workflows.md
  - template/SKILL.md
  - .claude-plugin/marketplace.json
  - spec/agent-skills-spec.md
  - README.md
---

# Research: Anthropic Skills Repository (github.com/anthropics/skills)

**Date**: 2026-01-28
**Branch**: main (repo), master (commandbase)
**Repo Commit**: `69c0b1a` — "Add link to Agent Skills specification website (#160)"

## Research Question

Full analysis of the official Anthropic skills repository — structure, skill-creator workflow, validation/packaging scripts, SKILL.md conventions, progressive disclosure patterns, marketplace plugin config, and bundled resource patterns across all 16 skills.

## Summary

The `anthropics/skills` repo is the **official reference implementation** for Claude skills. It contains 16 skills across creative, technical, enterprise, and document domains. The core value for skill creator tooling is the `skills/skill-creator/` directory, which defines a 6-step skill creation process with Python scripts (`init_skill.py`, `package_skill.py`, `quick_validate.py`) that scaffold, validate, and package skills into `.skill` files (zip with .skill extension).

The repo also serves as a **Claude Code Plugin marketplace** via `.claude-plugin/marketplace.json`, distributing skills as two plugin bundles: `document-skills` (4 proprietary) and `example-skills` (12 open source).

## Detailed Findings

### 1. Repository Structure

```
anthropics/skills/
├── .claude-plugin/
│   └── marketplace.json          # Plugin marketplace registration
├── .gitignore
├── README.md                      # Usage guide (Claude Code, claude.ai, API)
├── THIRD_PARTY_NOTICES.md
├── spec/
│   └── agent-skills-spec.md       # Points to https://agentskills.io/specification
├── template/
│   └── SKILL.md                   # Minimal template (4 lines)
└── skills/                        # 16 skill directories
    ├── algorithmic-art/           # Creative: p5.js generative art
    ├── brand-guidelines/          # Enterprise: Anthropic brand styling
    ├── canvas-design/             # Creative: PNG/PDF visual design
    ├── doc-coauthoring/           # Enterprise: doc collaboration workflow
    ├── docx/                      # Document: Word processing (proprietary)
    ├── frontend-design/           # Technical: production-grade UI
    ├── internal-comms/            # Enterprise: company communications
    ├── mcp-builder/               # Technical: MCP server creation
    ├── pdf/                       # Document: PDF manipulation (proprietary)
    ├── pptx/                      # Document: PowerPoint (proprietary)
    ├── skill-creator/             # Meta: skill creation guide
    ├── slack-gif-creator/         # Creative: Slack-optimized GIFs
    ├── theme-factory/             # Creative: artifact theming
    ├── webapp-testing/            # Technical: Playwright testing
    ├── web-artifacts-builder/     # Technical: React/Tailwind artifacts
    └── xlsx/                      # Document: Excel (proprietary)
```

### 2. Skill-Creator: The Core Workflow

**Location**: `skills/skill-creator/` (356 lines in SKILL.md)

The skill-creator defines a **6-step skill creation process**:

| Step | Action | Details |
|------|--------|---------|
| 1 | **Understand** | Gather concrete usage examples from user |
| 2 | **Plan** | Identify reusable resources (scripts, references, assets) |
| 3 | **Initialize** | Run `init_skill.py <name> --path <dir>` |
| 4 | **Edit** | Write SKILL.md, implement resources, test scripts |
| 5 | **Package** | Run `package_skill.py <path>` → produces `.skill` file |
| 6 | **Iterate** | Test with real tasks, refine |

#### 2.1 init_skill.py (scripts/init_skill.py)

**Purpose**: Scaffolds a new skill directory from embedded templates.

**Usage**: `init_skill.py <skill-name> --path <output-directory>`

**What it creates**:
```
<skill-name>/
├── SKILL.md                      # From SKILL_TEMPLATE (102 lines)
├── scripts/
│   └── example.py                # Placeholder (chmod 0o755)
├── references/
│   └── api_reference.md          # Placeholder reference doc
└── assets/
    └── example_asset.txt         # Placeholder asset file
```

**Key implementation details**:
- `title_case_skill_name()` — converts `my-skill` → `My Skill` (line 189-191)
- `init_skill()` — creates dir, writes SKILL.md, creates 3 resource dirs with examples (line 194-244)
- Fails if directory already exists (line 209-211)
- Generated SKILL.md contains extensive `[TODO:]` guidance including 4 structural patterns:
  1. **Workflow-Based** — sequential processes (DOCX pattern)
  2. **Task-Based** — tool collections (PDF pattern)
  3. **Reference/Guidelines** — standards/specs (brand-guidelines pattern)
  4. **Capabilities-Based** — integrated systems (product management pattern)

#### 2.2 package_skill.py (scripts/package_skill.py)

**Purpose**: Validates then zips a skill folder into a `.skill` distribution file.

**Usage**: `package_skill.py <path/to/skill-folder> [output-directory]`

**Process**:
1. Validates skill folder exists and is a directory
2. Checks `SKILL.md` exists
3. Calls `validate_skill()` from `quick_validate.py`
4. Creates a ZIP file with `.skill` extension
5. Uses `zipfile.ZIP_DEFLATED` compression
6. Archives all files with paths relative to skill's **parent** directory (line 62: `arcname = file_path.relative_to(skill_path.parent)`)
7. Output filename: `<skill-name>.skill` (in CWD or specified output dir)

**Important**: The zip maintains directory structure from parent level, so the `.skill` file contains `skill-name/SKILL.md`, not just `SKILL.md`.

#### 2.3 quick_validate.py (scripts/quick_validate.py)

**Purpose**: Validates skill structure and frontmatter.

**Validation checks (in order)**:

| # | Check | Condition | Error |
|---|-------|-----------|-------|
| 1 | SKILL.md exists | `skill_path / 'SKILL.md'` | "SKILL.md not found" |
| 2 | Frontmatter present | starts with `---` | "No YAML frontmatter found" |
| 3 | Frontmatter format | regex `^---\n(.*?)\n---` | "Invalid frontmatter format" |
| 4 | YAML parseable | `yaml.safe_load()` | "Invalid YAML in frontmatter" |
| 5 | Is dict | `isinstance(frontmatter, dict)` | "Frontmatter must be a YAML dictionary" |
| 6 | No unexpected keys | keys ⊆ ALLOWED_PROPERTIES | "Unexpected key(s)" |
| 7 | `name` present | `'name' in frontmatter` | "Missing 'name'" |
| 8 | `description` present | `'description' in frontmatter` | "Missing 'description'" |
| 9 | Name is string | `isinstance(name, str)` | Type error |
| 10 | Name format | regex `^[a-z0-9-]+$` | "should be hyphen-case" |
| 11 | Name edges | no start/end `-`, no `--` | "cannot start/end with hyphen" |
| 12 | Name length | `len(name) ≤ 64` | "Name is too long" |
| 13 | Description is string | `isinstance(description, str)` | Type error |
| 14 | No angle brackets | no `<` or `>` in description | "cannot contain angle brackets" |
| 15 | Description length | `len(description) ≤ 1024` | "Description is too long" |

**Allowed frontmatter properties**: `{'name', 'description', 'license', 'allowed-tools', 'metadata'}`

**Required**: `name`, `description`

**Depends on**: `pyyaml` (imported as `yaml`)

### 3. SKILL.md Frontmatter Conventions (All 16 Skills)

Every SKILL.md uses YAML frontmatter with `---` delimiters. Observed fields:

| Skill | name | description length | extra fields |
|-------|------|--------------------|--------------|
| algorithmic-art | `algorithmic-art` | 274 chars | `license` |
| brand-guidelines | `brand-guidelines` | 209 chars | `license` |
| canvas-design | `canvas-design` | 227 chars | `license` |
| doc-coauthoring | `doc-coauthoring` | 383 chars | (none) |
| docx | `docx` | 311 chars (quoted) | `license` |
| frontend-design | `frontend-design` | 338 chars | `license` |
| internal-comms | `internal-comms` | 274 chars | `license` |
| mcp-builder | `mcp-builder` | 233 chars | `license` |
| pdf | `pdf` | 213 chars | `license` |
| pptx | `pptx` | 248 chars (quoted) | `license` |
| skill-creator | `skill-creator` | 194 chars | `license` |
| slack-gif-creator | `slack-gif-creator` | 223 chars | `license` |
| theme-factory | `theme-factory` | 245 chars | `license` |
| webapp-testing | `webapp-testing` | 205 chars | `license` |
| web-artifacts-builder | `web-artifacts-builder` | 267 chars | `license` |
| xlsx | `xlsx` | 327 chars (quoted) | `license` |

**Patterns observed**:
- All names are hyphen-case, match their directory name exactly
- Descriptions range from 194-383 characters (all well under 1024 limit)
- 15/16 skills include a `license` field (doc-coauthoring is the exception)
- 3 skills (docx, pptx, xlsx) use YAML quoted strings for descriptions
- Document skills use `license: Proprietary. LICENSE.txt has complete terms`
- Open source skills use `license: Complete terms in LICENSE.txt`
- No skills use `allowed-tools` or `metadata` frontmatter fields
- **Description pattern**: "[What it does]. [When to use it / trigger conditions]."

### 4. Skill Body Size Distribution

| Lines | Skill | Category |
|-------|-------|----------|
| 483 | pptx | Document |
| 404 | algorithmic-art | Creative |
| 375 | doc-coauthoring | Enterprise |
| 356 | skill-creator | Meta |
| 294 | pdf | Document |
| 288 | xlsx | Document |
| 254 | slack-gif-creator | Creative |
| 236 | mcp-builder | Technical |
| 196 | docx | Document |
| 129 | canvas-design | Creative |
| 95 | webapp-testing | Technical |
| 73 | brand-guidelines | Enterprise |
| 73 | web-artifacts-builder | Technical |
| 59 | theme-factory | Creative |
| 42 | frontend-design | Technical |
| 32 | internal-comms | Enterprise |

The skill-creator's own guidance says to keep SKILL.md under 500 lines. All skills comply. The average is ~212 lines.

### 5. Bundled Resource Patterns Across Skills

Skills organize resources into 3 categories, but usage varies significantly:

| Pattern | Skills | Examples |
|---------|--------|----------|
| **SKILL.md only** | brand-guidelines, doc-coauthoring, frontend-design | No bundled resources |
| **SKILL.md + templates/** | algorithmic-art | `templates/viewer.html`, `templates/generator_template.js` |
| **SKILL.md + scripts/** | xlsx, webapp-testing, web-artifacts-builder | Scripts for execution |
| **SKILL.md + scripts/ + references/** | mcp-builder, skill-creator | Scripts + docs for progressive disclosure |
| **SKILL.md + scripts/ + reference docs** | pdf, docx, pptx | `forms.md`, `reference.md` at skill root + scripts/ |
| **SKILL.md + examples/** | internal-comms, webapp-testing | Example docs/scripts |
| **SKILL.md + themes/ + assets** | theme-factory, canvas-design | Theme definitions, fonts |
| **SKILL.md + core/** | slack-gif-creator | Python modules as `core/` instead of `scripts/` |

**Notable deviations from the standard `scripts/references/assets/` convention**:
- `algorithmic-art` uses `templates/` instead of `assets/`
- `slack-gif-creator` uses `core/` instead of `scripts/`
- `pdf` and `docx` put reference docs at skill root (`forms.md`, `reference.md`) not in `references/`
- `internal-comms` uses `examples/` instead of `references/`
- `theme-factory` uses `themes/` directory
- `canvas-design` has `canvas-fonts/` (90+ font files)
- `mcp-builder` uses `reference/` (singular) instead of `references/` (plural)

**The official skill-creator recommends** `scripts/`, `references/`, `assets/` but the actual skills in the same repo frequently use different naming.

### 6. Progressive Disclosure (Three-Level Loading)

The skill-creator defines a critical three-level system:

| Level | What | When loaded | Size constraint |
|-------|------|-------------|-----------------|
| 1 | Metadata (name + description) | **Always in context** | ~100 words |
| 2 | SKILL.md body | **When skill triggers** | <5k words, <500 lines |
| 3 | Bundled resources | **As needed by Claude** | Unlimited (scripts can execute without context) |

**Key insight**: The `description` field in frontmatter is the **primary triggering mechanism**. All "when to use" guidance must be in the description, not the body. The body is only loaded after the skill has already triggered.

### 7. Marketplace Plugin Configuration

**File**: `.claude-plugin/marketplace.json`

```json
{
  "name": "anthropic-agent-skills",
  "owner": { "name": "Keith Lazuka", "email": "klazuka@anthropic.com" },
  "metadata": { "description": "...", "version": "1.0.0" },
  "plugins": [
    {
      "name": "document-skills",
      "description": "...",
      "source": "./",
      "strict": false,
      "skills": ["./skills/xlsx", "./skills/docx", "./skills/pptx", "./skills/pdf"]
    },
    {
      "name": "example-skills",
      "description": "...",
      "source": "./",
      "strict": false,
      "skills": ["./skills/algorithmic-art", ... 12 skills total]
    }
  ]
}
```

**Installation**: Users register the marketplace then install plugins:
```bash
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

**Fields**:
- `strict: false` — skills are not strictly enforced (soft matching)
- `source: "./"` — skills are relative to repo root
- `skills` — array of paths to skill directories

### 8. The Template SKILL.md

**File**: `template/SKILL.md` (4 lines)

```yaml
---
name: template-skill
description: Replace with description of the skill and when Claude should use it.
---

# Insert instructions below
```

This is the **minimal** template. The `init_skill.py` generates a far more detailed template (102 lines) with structural guidance and TODO placeholders.

### 9. Agent Skills Specification

**File**: `spec/agent-skills-spec.md` — simply redirects to `https://agentskills.io/specification`

The spec is maintained externally, not in this repo. The validator enforces spec constraints:
- Name: max 64 characters, hyphen-case (`[a-z0-9-]+`)
- Description: max 1024 characters, no angle brackets

### 10. Core Design Principles from skill-creator SKILL.md

1. **"Concise is Key"** — Context window is a public good. Only add what Claude doesn't already know.
2. **"Degrees of Freedom"** — Match specificity to task fragility (high/medium/low freedom).
3. **"Progressive Disclosure"** — Three-level loading to minimize context bloat.
4. **"Don't create extraneous files"** — No README.md, CHANGELOG.md, etc. in skills.
5. **"Description is the trigger"** — All "when to use" info goes in frontmatter description.
6. **"Imperative form"** — SKILL.md uses imperative/infinitive writing style.
7. **"Test scripts by running them"** — Added scripts must be verified by execution.
8. **"Delete unused examples"** — Init generates scaffolding that should be pruned.

### 11. Reference Documents (Progressive Disclosure Examples)

#### output-patterns.md (skill-creator/references/)
Two patterns for consistent output:
- **Template Pattern** — strict (exact structure) or flexible (sensible defaults)
- **Examples Pattern** — input/output pairs for style matching

#### workflows.md (skill-creator/references/)
Two workflow patterns:
- **Sequential Workflows** — numbered step overview at top of SKILL.md
- **Conditional Workflows** — decision tree branching with labeled sub-workflows

## Code References

- `skills/skill-creator/SKILL.md:1-356` — Full skill creation guide
- `skills/skill-creator/scripts/init_skill.py:18-103` — SKILL_TEMPLATE string literal
- `skills/skill-creator/scripts/init_skill.py:189-191` — title_case_skill_name function
- `skills/skill-creator/scripts/init_skill.py:194-244` — init_skill function
- `skills/skill-creator/scripts/package_skill.py:26-78` — package_skill function
- `skills/skill-creator/scripts/package_skill.py:62` — arcname relative_to parent
- `skills/skill-creator/scripts/quick_validate.py:12-87` — validate_skill function
- `skills/skill-creator/scripts/quick_validate.py:42` — ALLOWED_PROPERTIES set
- `skills/skill-creator/scripts/quick_validate.py:65` — name regex pattern
- `skills/skill-creator/scripts/quick_validate.py:70` — max name length (64)
- `skills/skill-creator/scripts/quick_validate.py:84` — max description length (1024)
- `skills/skill-creator/references/output-patterns.md` — Template + Examples patterns
- `skills/skill-creator/references/workflows.md` — Sequential + Conditional patterns
- `.claude-plugin/marketplace.json` — Plugin marketplace registration
- `template/SKILL.md` — Minimal 4-line template

## Architecture Notes

### Skill Format = Directory, Not File
A skill is fundamentally a **directory** containing a `SKILL.md` file plus optional resources. The `.skill` distribution format is a **ZIP archive** of that directory. This is distinct from Claude Code commands/agents which are single markdown files.

### Dual Distribution Model
Skills can be distributed two ways:
1. **Plugin marketplace** — `.claude-plugin/marketplace.json` registers the repo as a marketplace, and users install bundles of skills via `/plugin install`
2. **`.skill` file** — `package_skill.py` creates a standalone zip that can be shared directly

### Validation as Gate, Not Continuous
The validator runs only at packaging time (`package_skill.py` calls `validate_skill`). There is no watch mode, CI integration, or pre-commit hook. This is a deliberate lightweight approach.

### The Naming Asymmetry
The skill-creator recommends `scripts/`, `references/`, `assets/` directory names, but skills in the same repo use `templates/`, `core/`, `examples/`, `themes/`, `reference/` (singular). The validator does not enforce directory naming — only frontmatter structure.

## Open Questions

1. The `allowed-tools` frontmatter field is in ALLOWED_PROPERTIES but no skill uses it. What does it control?
2. The `metadata` frontmatter field is allowed but unused. What is its intended purpose?
3. The `strict` field in marketplace.json is set to `false` for both plugins. What would `true` enforce?
4. The external spec at agentskills.io may define additional constraints not enforced by quick_validate.py — would need to fetch that spec to confirm.
5. How does Claude's skill triggering actually match the `description` field? Is it semantic matching, keyword matching, or embedding similarity?
