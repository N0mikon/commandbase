---
date: 2026-02-09
status: complete
topic: "workflow visualization methods for plugin documentation"
tags: [research, visualization, mermaid, diagrams, documentation, workflow, ASCII, interactive]
git_commit: ba0736e
---

# Workflow Visualization Methods for Plugin Documentation

## Research Question
What are the best methods for visually representing plugin/skill/agent/hook workflows in developer documentation? Including Mermaid diagrams, ASCII art, interactive docs, and other approaches for mapping interconnected tool chains.

## Summary
For the commandbase workflow map, **Mermaid flowcharts** are the strongest fit — they render natively on GitHub, live in version control, and handle the ~40-50 node range of our plugin system. The key constraint is O(n²) complexity: stay under 100 connections and 50 nodes per diagram, which means splitting the full system into 3-4 focused diagrams rather than one monolith. For richer visualization, **D2** produces more aesthetic output via ELK layout. For interactive exploration, **Docusaurus + React Flow** is the gold standard but requires a dedicated documentation site.

## Detailed Findings

### 1. Mermaid Diagrams (Best Fit for GitHub README)

**Verdict**: Primary recommendation for commandbase.

**Why it fits**:
- Native GitHub rendering — no build step, no images to maintain
- Text-based — version-controllable, diff-friendly
- Supports flowcharts, sequence diagrams, state diagrams, C4 architecture
- AI assistants can generate and iterate on Mermaid syntax efficiently

**Critical constraints**:
- **O(n²) complexity**: Flowcharts shouldn't exceed ~100 connections or ~50 nodes
- **GitHub limitations**: No Font Awesome icons, no hyperlinks in labels, no scaling control for large diagrams
- **ELK renderer** (available since v9.4) handles complex hierarchical graphs better than default Dagre, but may be slower
- Mermaid v11 moved ELK to a separate package to reduce bundle size

**Best practices for readability**:
- Use descriptive node IDs instead of single letters
- Define all nodes with labels first, then establish connections
- Use subgraphs to highlight logical groupings (e.g., per-plugin boundaries)
- Add `%%` comments to explain complex flows
- Use `classDef` for reusable styling (color-code by plugin or component type)
- Quote labels containing parentheses: `A-->B["Text (with parens)"]`
- Test at mermaid.live before committing

**Best diagram types for commandbase**:
- **Flowcharts**: BRDSPI chain flow, agent delegation, cross-plugin dependencies
- **Sequence diagrams**: Hook lifecycle (SessionStart → During → PreCompact → Stop)
- **State diagrams**: Session lifecycle (active → handed-off → ended)

**Splitting strategy**: One overview flowchart + detailed sub-diagrams:
1. Plugin dependency map (8 nodes, simple)
2. BRDSPI artifact flow (6 nodes + agent delegation ~20 connections)
3. Session lifecycle state diagram (~8 states)
4. Hook execution timeline (sequence diagram, 5 hooks)

### 2. D2 Language (Best Aesthetics)

**Verdict**: Strong alternative if GitHub rendering isn't required.

**Advantages over Mermaid**:
- "Most aesthetic and readable diagrams" using ELK layout engine
- First-class container support for nested groupings
- Production-ready themes for professional output
- CLI produces SVGs from .d2 files
- Extensions for VS Code, Vim, Obsidian

**Disadvantage**: Requires compilation to SVG — not GitHub-native. Would need to commit rendered images or use a docs site.

### 3. ASCII/Unicode Art (Terminal-Compatible)

**Verdict**: Good for inline code blocks showing simple flows, not for complex maps.

**Tools**:
- **ASCIIFlow** (asciiflow.com): Browser-based editor, exports pure text
- **Graph-Easy** (Perl): Text input → ASCII art flowcharts with Unicode box-drawing
- **Boxes CLI**: Command-line tool for ASCII art boxes
- **Ditaa**: Converts ASCII art to bitmap/vector graphics

**Best practices**:
- ASCII borders (`-`, `|`, `+`) for maximum cross-platform compatibility
- Unicode box-drawing (U+2500–U+257F: `┌─┐`, `├─┤`, `└─┘`) for cleaner look in modern terminals
- Monospaced fonts required for alignment
- Works best for simple linear flows (5-10 boxes), not complex interconnected systems

**Recommendation for commandbase**: Use ASCII for inline quick-reference flows in SKILL.md files (e.g., "B → R → D → S → P → I"), Mermaid for architectural diagrams in README.

### 4. PlantUML (UML Precision)

**Verdict**: Overkill for commandbase. Better for formal system architecture in regulated environments.

**How it compares to Mermaid**:
- Mermaid "optimizes for speed and approachability" — easy syntax, native GitHub support
- PlantUML "optimizes for precision and full UML coverage" — steeper learning curve, Java-based
- **Community consensus**: "Many teams keep both: Mermaid for narrative docs, PlantUML for formal system diagrams"
- PlantUML has more diagram types and customization but requires server-side rendering

### 5. Interactive Documentation (Future Option)

**Verdict**: Worth considering if commandbase grows to need a docs site.

**Approaches**:
- **Docusaurus + Mermaid plugin**: React-based docs with embedded diagrams, versioning, search
- **MkDocs Material + Markmap**: Python-based, YAML config, mind map visualization from markdown
- **React Flow / Xyflow**: Node-based interactive UIs — Stripe uses this for process documentation
- **Docsify**: Zero-build-step docs from README (simplest migration path)

**Decision framework**:
- **Simple projects**: README + embedded Mermaid (← commandbase is here now)
- **Medium complexity**: README + `/docs` folder browsable on GitHub
- **Complex projects**: Dedicated docs site (Docusaurus, MkDocs)

**AI agent framework patterns** (from LangChain, CrewAI, AutoGen):
- LangChain documents 6 workflow patterns each with diagram + code: prompt chaining, parallelization, routing, orchestrator-worker, evaluator-optimizer, agents
- CrewAI offers `crewai flow plot` — generates HTML visualization of flow structure
- AutoGen uses step-by-step flow diagrams showing message receipt → code generation → execution → termination

### 6. Markmap (Mind Maps from Markdown)

**Verdict**: Interesting for hierarchical overview (plugin → skills → agents), but not ideal for workflow flows.

**What it does**: Converts markdown headings into interactive mind maps. Version-controllable, integrates with MkDocs, VS Code, Obsidian.

### 7. Practical Recommendations for commandbase

**Immediate (README-level)**:
Use 3-4 Mermaid diagrams in README or a new `docs/ARCHITECTURE.md`:

1. **Plugin Dependency Map** (flowchart, ~10 nodes):
   ```
   core → code, vault, services, research, git-workflow, session
   meta → standalone
   ```

2. **BRDSPI Artifact Flow** (flowchart, ~15 nodes):
   ```
   brainstorm → research → design → structure → plan → implement
   with docs-writer spawns and staleness detection arrows
   ```

3. **Session Lifecycle** (state diagram, ~8 states):
   ```
   [*] → starting → active → {merge|handoff|discard} → ended
   active → resuming → active
   ```

4. **Hook Timeline** (sequence diagram, 5 participants):
   ```
   SessionStart → PostToolUseFailure → PreCompact → Stop
   with data flows to errors.log, meta.json
   ```

**Future (docs site)**:
If the project grows, migrate to Docusaurus with Mermaid plugin + React Flow for interactive exploration.

## Source Conflicts

- **C4 diagram maturity**: Some sources recommend C4 for architectural overview (experimental in Mermaid), others call it "unwieldy" and suggest alternatives. For commandbase, standard flowcharts are clearer than C4.
- **Mermaid vs D2**: D2 produces more aesthetic output, but Mermaid's GitHub-native rendering makes it the pragmatic choice for README documentation.

## Currency Assessment

- Most recent sources: 2025-2026
- Topic velocity: Fast-moving (Mermaid v11 restructured, D2 actively evolving)
- Confidence in currency: High — multiple 2026 sources cross-referenced

## Key Sources

- [Mermaid O(n²) complexity](https://mermaid.ai/docs/blog/posts/flow-charts-are-on2-complex-so-dont-go-over-100-connections) — Official Mermaid docs
- [GitHub Mermaid Support](https://github.blog/developer-skills/github/include-diagrams-markdown-files-mermaid/) — GitHub Blog
- [D2 Language](https://d2lang.com/) — Official docs
- [Mermaid vs PlantUML 2026](https://www.gleek.io/blog/mermaid-vs-plantuml) — Gleek.io comparison
- [Diagrams as Code](https://simmering.dev/blog/diagrams/) — Paul Simmering
- [LangChain Workflow Patterns](https://docs.langchain.com/oss/python/langgraph/workflows-agents) — Official docs
- [CrewAI Flow Plot](https://docs.crewai.com/en/guides/flows/first-flow) — Official docs
- [React Flow](https://reactflow.dev) — Official site
- [Command Line Interface Guidelines](https://clig.dev/) — Community standard
- [Docusaurus Diagrams](https://docusaurus.io/docs/next/markdown-features/diagrams) — Official docs

## Open Questions

- Should commandbase diagrams live in root README, per-plugin READMEs, or a separate ARCHITECTURE.md?
- Is the ELK renderer available in GitHub's Mermaid rendering, or only in self-hosted/docs-site contexts?
- Would a Markmap mind map of the full plugin/skill hierarchy complement the Mermaid workflow diagrams?
