---
date: 2026-02-12
status: complete
topic: "axton-obsidian-visual-skills Repository Analysis"
tags: [research, repo-analysis, claude-code-skills, obsidian, excalidraw, mermaid, canvas, plugin-marketplace]
git_commit: 9c4c7f4
references:
  - .claude-plugin/marketplace.json
  - excalidraw-diagram/SKILL.md
  - mermaid-visualizer/SKILL.md
  - obsidian-canvas-creator/SKILL.md
---

## Overview

**Repository:** axton-obsidian-visual-skills
**Author:** Axton Liu (axtonliu.ai)
**License:** MIT
**Version:** marketplace.json v0.1.0, excalidraw skill v1.2.1
**Status:** Experimental

A Claude Code plugin marketplace package containing a single plugin (`obsidian-visual-skills`) with 3 visual diagram generation skills for Obsidian. Generates Canvas, Excalidraw, and Mermaid diagram files from text descriptions with bilingual (English/Chinese) support.

**Repository source:** `/c/code/repo-library/vault-repos/axton-obsidian-visual-skills/`

## Repository Structure

```
axton-obsidian-visual-skills/
├── .claude-plugin/
│   └── marketplace.json              # Plugin marketplace manifest
├── assets/                           # Demo screenshots for README
│   ├── canvas-demo.png
│   ├── excalidraw-demo.png
│   └── mermaid-demo.png
├── excalidraw-diagram/               # Skill 1 (437 lines)
│   ├── SKILL.md
│   └── references/
│       └── excalidraw-schema.md      # JSON schema, color palette, element types
├── mermaid-visualizer/               # Skill 2 (273 lines)
│   ├── SKILL.md
│   └── references/
│       └── syntax-rules.md           # Syntax reference, error prevention (484 lines)
├── obsidian-canvas-creator/          # Skill 3 (204 lines)
│   ├── SKILL.md
│   ├── assets/
│   │   ├── template-freeform-grouped.canvas  # Freeform layout template
│   │   └── template-mindmap-simple.canvas    # MindMap layout template
│   └── references/
│       ├── canvas-spec.md            # JSON Canvas specification (404 lines)
│       └── layout-algorithms.md      # Layout algorithm documentation (615 lines)
├── .gitignore                        # Excludes CLAUDE.md, DEVLOG.md
├── LICENSE                           # MIT
├── README.md                         # English documentation
└── README_CN.md                      # Chinese documentation
```

**Total non-git files:** 16 (3 SKILL.md, 5 reference docs, 2 canvas templates, 3 demo images, 2 READMEs, 1 LICENSE)

## Plugin Marketplace Format

The marketplace manifest uses a flat structure:

```json
{
  "name": "axton-obsidian-visual-skills",
  "owner": { "name": "Axton Liu", "email": "hey@axtonliu.com" },
  "metadata": {
    "description": "Visual Skills Pack for Obsidian...",
    "version": "0.1.0"
  },
  "plugins": [{
    "name": "obsidian-visual-skills",
    "description": "Generate Canvas, Excalidraw, and Mermaid diagrams in Obsidian",
    "source": "./",
    "skills": [
      "./excalidraw-diagram",
      "./mermaid-visualizer",
      "./obsidian-canvas-creator"
    ]
  }]
}
```

Key observations:
- Single plugin bundles all 3 skills together
- `source: "./"` — skills live at repository root, not nested in a plugin directory
- Skills referenced by relative directory path (each must contain SKILL.md)
- No agents, hooks, or setup files defined
- `skills` array in the plugin object — note: this may not be a standard marketplace field (commandbase uses a different structure)

## Skill Analysis

### 1. Excalidraw Diagram Generator (excalidraw-diagram)

**Complexity:** Most complex skill (437 lines + 202-line schema reference)
**Language:** Heavily bilingual — Chinese prose throughout workflow instructions, tables, and user-facing output

**Three output modes:**
| Trigger | Mode | Extension | Platform |
|---------|------|-----------|----------|
| `Excalidraw`, `画图`, `流程图` | Obsidian (default) | `.md` | Obsidian vault |
| `标准Excalidraw`, `standard excalidraw` | Standard | `.excalidraw` | excalidraw.com |
| `Excalidraw动画`, `animate` | Animated | `.excalidraw` | excalidraw-animate |

**8 diagram types:** Flowchart, Mind Map, Hierarchy, Relationship, Comparison, Timeline, Matrix, Freeform

**Key prompt engineering patterns:**
- Constraint enforcement via repetition — field requirements stated in 3+ locations
- Formula-based calculations for text centering (character width estimation)
- Negative constraint patterns — explicit "Do NOT include" field lists and "Common Mistakes to Avoid" section
- Mode-specific source URLs — Obsidian uses excalidraw-plugin GitHub URL vs excalidraw.com
- Auto-save workflow — 6-step process from type selection to user notification
- Obsidian-specific formatting: `excalidraw-plugin: parsed` frontmatter, `%%` comment wrappers, `==highlight==` warning banner

**Reference material:** Single schema file with color palette, 6 element types (rectangle, text, arrow, ellipse, diamond, line), font families (1-5, with 5=Excalifont), fill styles, roundness types, and element/arrow binding patterns.

### 2. Mermaid Visualizer (mermaid-visualizer)

**Complexity:** Medium (273 lines + 484-line syntax reference)
**Language:** English-only body, Chinese only in trigger words

**6 diagram types:** Process Flow (graph TB/LR), Circular Flow, Comparison, Mindmap, Sequence, State

**Key prompt engineering patterns:**
- Critical syntax rules with ✅/❌ examples — 5 named rules addressing common Mermaid parsing failures
- High configurability — 4 layouts x 4 detail levels x 4 styles = 64 combinations
- Semantic color coding — 9 color pairs mapped to functional meanings
- Quality checklist — 9-item pre-output validation
- Quick Start + detailed Workflow sections — dual-level guidance

**Notable syntax error prevention:**
- Rule 1: `[1. Perception]` triggers "Unsupported markdown: list" → use `[1.Perception]` or `[① Perception]`
- Rule 2: Subgraph naming must use `subgraph id["Display Name"]` pattern
- Rule 3: Always reference nodes by ID, not display name
- Character replacement: `"` → `『』`, `()` → `「」`

**Reference material:** Comprehensive syntax rules file covering node types, subgraph syntax, arrow types, styling, layout control, 5 advanced patterns (feedback loop, swimlane, hub-and-spoke, decision tree, comparison), and platform-specific rendering notes.

### 3. Obsidian Canvas Creator (obsidian-canvas-creator)

**Complexity:** Simplest SKILL.md (204 lines) but heaviest references (404 + 615 = 1,019 lines)
**Language:** English-only body, Chinese only in trigger words

**2 layout modes:**
- **MindMap** — Radial hierarchy from center (brainstorming, topic exploration)
- **Freeform** — Custom positioning with groups (complex networks, non-hierarchical)

**Key prompt engineering patterns:**
- Decision-oriented workflow — "When to Use" → layout determination → plan structure
- Content-based node sizing — 4 size categories by character count (30/60/100 char thresholds)
- Geometric validation — spacing minimums (320px horizontal, 200px vertical between centers)
- Z-index ordering — groups first (bottom), subgroups, then text nodes (top)
- ID generation — 8-12 character random hex strings
- Pure JSON output — no additional explanation text

**Template files:** Two working `.canvas` JSON examples demonstrating:
- `template-mindmap-simple.canvas` — Root node + branches + details with color hierarchy (green→cyan→purple)
- `template-freeform-grouped.canvas` — Group backgrounds + distributed nodes + labeled cross-group edges

**Reference materials:**
- `canvas-spec.md` — JSON Canvas spec with 4 node types (text, file, link, group), edge format, 6 preset colors + custom hex, validation rules, Chinese encoding notes
- `layout-algorithms.md` — Radial tree algorithm, grid-based zone layout, force-directed layout, collision detection formulas, spacing constants, quality checks

## Cross-Skill Patterns

### Shared conventions across all three skills:

1. **Frontmatter:** YAML with `name` (matching directory) and `description` (with trigger phrases). Only excalidraw adds `metadata.version`.
2. **No Emoji rule:** All three explicitly prohibit emoji in output — use color/shape differentiation instead.
3. **Chinese quote transformation:** All handle `"` → `『』` and `()` → `「」` for JSON compatibility.
4. **Reference separation:** Complex technical details in dedicated `references/` subdirectory files, linked from SKILL.md.
5. **Validation checklists:** Pre-output verification steps (excalidraw: field validation, mermaid: syntax validation, canvas: geometric validation).
6. **Semantic color coding:** All use meaningful color assignment (not random).

### Key differences:

| Aspect | Excalidraw | Mermaid | Canvas |
|--------|-----------|---------|--------|
| Output format | JSON in .md wrapper or .excalidraw | Mermaid code fence | Pure JSON .canvas |
| Error focus | Field validation | Syntax parsing | Geometric spacing |
| Configuration | Mode-based (3 modes) | Parameter-based (64 combos) | Binary (2 layouts) |
| Bilingual depth | Deep (Chinese prose) | Shallow (triggers only) | Shallow (triggers only) |
| Reference files | 1 (schema) | 1 (syntax rules) | 2 (spec + algorithms) |
| Templates | None | Inline code examples | 2 .canvas files |

## Relevance to commandbase-vault

### Patterns worth noting for vault skill development:

1. **Reference material organization** — Each skill keeps specs/schemas in `references/` subdirectory. This is similar to commandbase's `reference/` pattern but uses a different directory name.

2. **Template-driven output** — Canvas skill uses template .canvas files as examples for the LLM. This "show don't tell" approach could inform how vault skills provide example outputs.

3. **Multi-mode skills** — Excalidraw's 3-mode architecture (Obsidian/Standard/Animated) triggered by keyword detection is a pattern commandbase skills don't currently use but could adopt for skills with variant outputs.

4. **Obsidian-native formatting** — The excalidraw skill demonstrates deep knowledge of Obsidian plugin integration (frontmatter keys, comment syntax, plugin-specific source URLs). This level of Obsidian awareness could inform vault skills.

5. **Geometric validation patterns** — Canvas skill's spacing/overlap checks show how to enforce spatial relationships in generated content.

6. **Marketplace format difference** — This repo uses a `skills` array inside each plugin object, which differs from commandbase's directory-scanning approach. Worth verifying which format is canonical.
