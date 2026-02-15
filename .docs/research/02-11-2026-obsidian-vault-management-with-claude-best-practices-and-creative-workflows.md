---
date: 2026-02-11
status: complete
topic: "Obsidian vault management with Claude - best practices and creative workflows"
tags: [research, obsidian, claude, vault-management, mcp, ai-workflows]
git_commit: 9c4c7f4
---

# Obsidian Vault Management with Claude: Best Practices & Creative Workflows

## Research Question
What are the best practices and unique ideas for managing an Obsidian vault with Claude (via MCP, Claude Code, or plugins)?

## Summary
The Claude + Obsidian ecosystem has matured significantly in 2025-2026, with three primary integration paths: MCP servers (obsidian-mcp-tools, mcp-obsidian-advanced), embedded plugins (Claudian, Agent Client), and direct Claude Code filesystem access. Community consensus favors treating vaults as "codebases" with CLAUDE.md context files, shallow folder hierarchies with numeric prefixes, flat frontmatter schemas, and template-driven AI workflows. The most effective approaches combine git version control, atomic notes with rich wikilinks, and semi-automated workflows where AI suggests but humans curate.

## Detailed Findings

### 1. Integration Architecture Options

**MCP Servers** (standard protocol approach):
- **obsidian-mcp-tools** (jacksteamdev): Semantic search via Smart Connections, Templater integration, secure bridge architecture. Requires Obsidian running with Local REST API plugin.
- **mcp-obsidian-advanced** (ToKiDoO): 16 tools including NetworkX graph analysis, batch operations, vault intelligence. Published Feb 2026.
- **obsidian-claude-code-mcp** (iansinnott): WebSocket + HTTP/SSE dual transport, auto-discovery on port 22360. Claude Code finds running vaults automatically.
- **mcp-obsidian** (MarkusPfundstein): REST API-based, 7 core tools (list, get, search, patch, append, delete). Simple and reliable.

**Embedded Plugins** (native Obsidian UI):
- **Claudian** (YishenTu): Full Claude Code SDK embedded in sidebar. Read/write/search/bash. Three permission modes (YOLO/Safe/Plan). 52 vault actions.
- **Agent Client** (RAIT-09): Agent Client Protocol (ACP) by Zed Industries. Supports Claude Code, Codex, Gemini CLI. Multi-agent switching.

**Direct Filesystem** (Claude Code in terminal):
- Treat vault as a codebase. `cd` into vault, use CLAUDE.md for context. Works with vault closed. Simplest setup but bypasses Obsidian plugin features.

**Sources:** [GitHub - obsidian-mcp-tools](https://github.com/jacksteamdev/obsidian-mcp-tools), [GitHub - mcp-obsidian-advanced](https://github.com/ToKiDoO/mcp-obsidian-advanced), [GitHub - obsidian-claude-code-mcp](https://github.com/iansinnott/obsidian-claude-code-mcp), [GitHub - claudian](https://github.com/YishenTu/claudian), [GitHub - agent-client](https://github.com/RAIT-09/obsidian-agent-client)

### 2. CLAUDE.md as Vault Constitution

The single most impactful practice: a CLAUDE.md file at vault root that defines all conventions. Loaded automatically every session.

**What to include:**
- Vault purpose and personal context (name, role)
- Folder structure with explanations
- File naming conventions (e.g., `YYYY-MM-DD ddd` for dailies)
- Tagging taxonomy rules
- Linking conventions (wikilinks, when to create new notes)
- Frontmatter schema (required/optional properties per note type)
- Tone preferences
- Forbidden actions (what NOT to do)

**Pro tip:** Ask Claude to help write it: "Help me create my CLAUDE.md file for this Obsidian vault. Ask me questions about how I would like to use this vault. Use the existing file structure and metadata as a guide."

One user reported their CLAUDE.md grew from 3 lines to 370+ as they refined workflows.

**Sources:** [Teaching Claude Code My Obsidian Vault](https://mauriciogomes.com/teaching-claude-code-my-obsidian-vault), [Using Claude Code with Obsidian](https://kyleygao.com/blog/2025/using-claude-code-with-obsidian/), [GitHub - obsidian-claude-code](https://github.com/ashish141199/obsidian-claude-code)

### 3. Vault Structure Best Practices

**Consensus: Shallow hierarchy, numeric prefixes, flat notes with rich linking.**

**Recommended structure (AI-native):**
```
0xx - OS/meta (templates, CLAUDE.md, skills)
1xx - Periodics (daily, weekly, monthly, quarterly)
2xx - Notes/writing/AI logs
3xx - Entities (people, teams, goals, projects)
4xx - Resources (books, podcasts, web, courses)
9xx - Review/triage (unclassified)
```

**Alternative (project-oriented):**
```
00-inbox/        # Capture point
01-todos/        # Task tracking
02-projects/     # Project-specific context with CLAUDE.md
03-resources/    # Processed knowledge
04-claude-code/  # Claude configurations & skills
05-prompts/      # Prompt patterns
_templates/      # Obsidian templates
_assets/         # Images and attachments
```

**Key principles:**
- 1-2 levels max depth. Deep nesting confuses both humans and AI.
- Folders for note TYPE classification (a note can only belong to one folder).
- Tags for THEMATIC connections (a note has many themes).
- Aggressive wikilink usage over folder hierarchy.
- Steph Ango (Obsidian CEO): "Avoid folders for organization" — use quick switcher, backlinks, links.

**Sources:** [AI-Native Obsidian Vault Setup Guide](https://www.curiouslychase.com/posts/ai-native-obsidian-vault-setup-guide), [Knowledge Vault Structure](https://gist.github.com/naushadzaman/164e85ec3557dc70392249e548b423e9), [Steph Ango's Vault](https://stephango.com/vault)

### 4. Frontmatter Schema Design

**Critical constraint:** Obsidian Properties don't support nested YAML. Use flat, descriptive field names.

**Core schema:**
```yaml
---
type: [daily|weekly|person|project|moc|resource]
date: YYYY-MM-DD
tags:
  - topic
  - status/active
aliases:
  - alternate name
---
```

**Extended fields by note type:**
- Resources: `source`, `author`, `rating` (1-7 scale)
- People: `role`, `org`, `last-contact`
- Projects: `status`, `area`, `deadline`

**Design rules:**
- Default to `list` type properties if there's any chance of multiple values
- Short property names for faster typing
- Property names and values should be reusable across categories
- Use `status/` prefixed tags for workflow state: `status/to-evaluate` → `status/evaluated` → `status/adopted`

**Sources:** [Nested YAML Frontmatter for Obsidian](https://bbbburns.com/blog/2025/07/nested-yaml-frontmatter-for-obsidian-book-notes/), [Steph Ango's Vault](https://stephango.com/vault)

### 5. Tagging Taxonomy

**Nested tag system enables AI filtering:**

```
#insight/pattern, #insight/trigger, #insight/strength, #insight/growth-edge
#people/feedback-given, #people/praise-given, #people/conflict, #people/connection
#ai/prompt, #ai/agent, #ai/workflow, #ai/tool, #ai/limitation, #ai/surprise
#status/to-evaluate, #status/evaluated, #status/adopted
```

**Rules:**
- Always pluralize tag categories
- Max 5 tags per note to avoid clutter
- Use property-based tags (YAML frontmatter) for AI compatibility
- Nested tags create queryable hierarchies (`#ai/*` matches all AI-related)

**Sources:** [AI-Native Obsidian Vault Setup Guide](https://www.curiouslychase.com/posts/ai-native-obsidian-vault-setup-guide)

### 6. Obsidian-Specific Markdown Claude Must Know

**Official obsidian-skills repo** (kepano, 9.6k stars) provides skills for Claude:

**Wikilinks:** `[[Note]]`, `[[Note|Alias]]`, `[[Note#Heading]]`, `[[Note#^block-id]]`
**Embeds:** `![[Note]]`, `![[image.png|640x480]]`, `![[document.pdf#page=3]]`
**Callouts:** `> [!note]`, `> [!tip] Title`, `> [!warning]+` (foldable expanded), `> [!danger]-` (foldable collapsed)
**Properties:** YAML frontmatter with `type`, `tags`, `date`, `aliases`
**Dataview:** `TABLE field FROM #tag WHERE condition SORT field DESC`

**Installation:** Add obsidian-skills to `/.claude` folder in vault root, or `/plugin install obsidian@obsidian-skills`.

**Sources:** [GitHub - kepano/obsidian-skills](https://github.com/kepano/obsidian-skills), [Obsidian Callouts Help](https://help.obsidian.md/Editing+and+formatting/Callouts)

### 7. Creative Workflow Ideas

**Daily trigger architecture:**
- `/today` command pulls yesterday's content, GitHub PRs, legacy notes → generates tasks
- Evening `/wrapup` summary with auto-commit
- Weekly review: Reflect → Connect → Plan (60-90 min block)

**Automated backlinking:**
- "Read my journal entry and add backlinks to all people, places, and books mentioned. Search vault for existing entity notes, create new ones if needed."

**Batch processing:**
- Metadata normalization across vault
- Backlink insertion for orphan notes
- Transform orphaned notes into knowledge graph connections
- Rename files to remove spaces/special characters
- Convert dataview metadata to Obsidian Bases format

**MOC auto-generation:**
- Dataview queries that auto-maintain MOCs: `LIST FROM #tagname`
- AI-powered topic modeling to suggest MOC groupings
- `/find-connections` discovers non-obvious relationships via graph traversal

**Voice → structured notes:**
- Scribe plugin: record, transcribe (Whisper/AssemblyAI), transform into structured insights with summaries, action items, Mermaid charts
- SuperWhisper + Claude: dictation → automatic organization into correct vault location

**AI-powered spaced repetition:**
- True Recall plugin: FSRS v6 algorithm, AI generates flashcards following SuperMemo's 20 rules
- Cards link back to originating notes for context

**Research compilation:**
- Aggregate info from multiple sources (URLs, personal notes) into unified reports
- Eleanor Konik: processed 15-million-word knowledge base overnight (indices, metadata fixes, RSS encoding corrections)

**Decision framework application:**
- Before major decisions, prompt Claude to apply mental models checklists systematically
- Investment post-mortems: compare original thesis against outcomes

**Sources:** [Obsidian x Claude Code: The Ultimate Workflow Guide](https://www.axtonliu.ai/newsletters/ai-2/posts/obsidian-claude-code-workflows), [Eleanor Konik: Claude + Obsidian](https://www.eleanorkonik.com/p/how-claude-obsidian-mcp-solved-my), [True Recall FSRS plugin](https://forum.obsidian.md/t/i-built-a-native-fsrs-algorithm-for-obsidian-with-ai-flashcard-generation/109962), [GitHub - Scribe](https://github.com/Mikodin/obsidian-scribe)

### 8. Quality Control & Safety

**Git is mandatory before enabling AI write access.**

- Git backup before every batch edit
- Git diff review of all Claude modifications
- Tag AI-generated content with markers (e.g., `<ai-suggestion>`)
- Start with read-only queries, enable writes incrementally
- Sandbox approach: test in separate vaults before production
- Canvas flowcharts as executable instructions (visual prompting)

**Community consensus:** "MCP works best as an exploratory tool rather than a permanent workflow enhancement. Most experienced users haven't enabled it permanently in their main vaults due to token limitations and the labor-intensive experimentation required."

**Sources:** [Obsidian Forum: MCP Experiences](https://forum.obsidian.md/t/obsidian-mcp-servers-experiences-and-recommendations/99936), [Obsidian x Claude Code Workflow Guide](https://www.axtonliu.ai/newsletters/ai-2/posts/obsidian-claude-code-workflows)

### 9. Slash Commands & Template Systems

**`.claude/commands/` directory** stores reusable workflows:
- `/day` — create/open daily note
- `/research "topic"` — research and create interconnected notes
- `/brainstorm "topic"` — generate and organize ideas
- `/tag-file` — analyze note and add appropriate tags
- `/tag-folder` — batch-tag all files in a directory
- `/digest` — transform inbox links into structured notes
- `/mise-en-place` — week setup: run script, review North Star, prepare check-ins

**Smart Templates plugin:** Drop markdown files in templates folder with EJS variables (`{{topic}}`, `{{tone}}`). Local-first, supports Anthropic Claude, OpenAI, Gemini, local models.

**Multi-step prompt chains:** Keyword research → outline generation → drafting → optimization review, each step auto-including previous outputs.

**Sources:** [GitHub - obsidian-claude-code](https://github.com/ashish141199/obsidian-claude-code), [GitHub - Smart Templates](https://github.com/brianpetro/obsidian-smart-templates), [AI-Native Vault Setup](https://www.curiouslychase.com/posts/ai-native-vault-setup-guide)

### 10. Integration Path Comparison (Deep Dive)

Parallel research across all three integration paths produced a decision matrix for choosing the right approach.

#### MCP Servers — Detailed Assessment

**Implementations compared:**
- **cyanheads/obsidian-mcp-server**: 8 tools, v2.0.7, 187 commits. Most mature. Docker support. Tools: read_note, update_note, search_replace, global_search, list_notes, manage_frontmatter, manage_tags, delete_note.
- **mcp-obsidian-advanced** (ToKiDoO): 16 tools. JsonLogic queries, NetworkX graph objects, batch read, periodic notes, Dataview queries, Obsidian command execution. Requires Python + uv.
- **obsidian-mcp-tools** (jacksteamdev): Semantic search via Smart Connections embeddings, Templater template execution. Automated installer. v0.2.27.
- **obsidian-claude-code-mcp** (iansinnott): Auto-discovery via port 22360. Dual transport (WebSocket for Claude Code, HTTP/SSE for Claude Desktop). IDE-style features (diffs, diagnostics, tab management).
- **mcp-obsidian** (MarkusPfundstein): 7 core tools. Lightweight, well-documented. Python + uv required.

**Common requirements:** Obsidian running + Local REST API plugin + API key + Node.js or Python runtime.

**Key weaknesses:** 5-10 min latency on large vaults (3000+ notes). 10-min cache staleness. Token exhaustion with vault-wide visibility. Windows path handling inconsistencies. No per-tool permission model. Community fragmentation (no canonical server).

**Sources:** [GitHub - cyanheads/obsidian-mcp-server](https://github.com/cyanheads/obsidian-mcp-server), [GitHub - ToKiDoO/mcp-obsidian-advanced](https://github.com/ToKiDoO/mcp-obsidian-advanced), [GitHub - MarkusPfundstein/mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian)

#### Embedded Plugins — Detailed Assessment

**Claudian** (YishenTu):
- v1.3.63 (Feb 7, 2026). Multiple releases per day — suggests rapid iteration but potential instability.
- 52+ vault actions via natural language. Model orchestration (Haiku/Sonnet/Opus routing). Vision analysis.
- Skills compatible with Claude Code format. MCP server support as extension.
- **Not in Obsidian Community Plugins.** PR was closed (stale) due to naming conflict — "dian" flagged as too similar to "Obsidian."
- Install via BRAT or manual file copy. Requires Claude Code CLI.
- Known issues: Windows/WSL CLI discovery failures, hot-reload unsupported, iCloud vault loading problems, silent file modification failures.

**Agent Client** (RAIT-09):
- v0.8.0-preview.1 (Feb 7, 2025). Agent Client Protocol (ACP) by Zed Industries.
- Supports Claude Code, Codex, Gemini CLI, custom agents. Multi-agent switching (not simultaneous).
- **Not in Obsidian Community Plugins.** Pending review with 25+ code quality issues: innerHTML security risks, missing await expressions, improper DOM patterns, unused variables.
- Install via BRAT. Requires absolute paths to Node.js and agent binaries.

**Key difference from MCP:** Embedded plugins bundle AI interface inside Obsidian UI (monolithic). MCP is protocol-based middleware (composable). Claudian wraps Claude Code; MCP exposes vault as tools any client can use.

**Sources:** [GitHub - YishenTu/claudian](https://github.com/YishenTu/claudian), [GitHub - RAIT-09/obsidian-agent-client](https://github.com/RAIT-09/obsidian-agent-client), [Obsidian Releases PR #9046](https://github.com/obsidianmd/obsidian-releases/pull/9046)

#### Direct Filesystem — Detailed Assessment

**How it works:** `cd /path/to/vault && claude`. Claude uses Read, Write, Edit, Grep, Glob, Bash directly on markdown files. CLAUDE.md auto-loaded for conventions.

**Proven at scale:**
- Eleanor Konik: processed 15M-word knowledge base overnight (organizational indices, metadata fixes, RSS encoding corrections). All changes via git commits.
- Kyle Gao: "read journal entry, add backlinks to people/places/books" — 15 seconds.
- Mauricio Gomes: CLAUDE.md grew from 3 to 370+ lines. Claude learned to place entries in `~/work-log/2025/2025-08/2025-08-09.md` without asking.
- Reddit user: "I had just totally spaced that Obsidian is just files on disk and Claude can totally do all of that with no fuss in like 30 seconds."

**Key advantage for commandbase:** Skills/agents/hooks work natively. Vault is just another codebase. Same `/committing-changes`, `/starting-session` workflow. No abstraction layer.

**Key limitation:** No Obsidian plugin access (Templater, Dataview, Smart Connections). Keyword Grep only — no semantic search. Must handle wikilink resolution manually.

**Sources:** [Eleanor Konik: Claude + Obsidian Got a Level Up](https://www.eleanorkonik.com/p/claude-obsidian-got-a-level-up), [Using Claude Code with Obsidian](https://kyleygao.com/blog/2025/using-claude-code-with-obsidian/), [Teaching Claude Code My Obsidian Vault](https://mauriciogomes.com/teaching-claude-code-my-obsidian-vault)

#### Decision Matrix

| Criteria | MCP Servers | Embedded Plugins | Direct Filesystem |
|----------|------------|-----------------|-------------------|
| **Setup / maintenance** | Moderate — Obsidian + REST API + server config | Weak — BRAT install, not in registry, daily releases | **Strong** — zero deps, works immediately |
| **Vault operations** | **Strong** — semantic search, Templater, graph, 16+ tools | **Strong** — 52 actions, auto-tagging, vision, model routing | Moderate — powerful bulk ops, no semantic search |
| **Commandbase compatibility** | Moderate — MCP tools via ToolSearch, adds abstraction | Weak — duplicates CLI, skills don't translate cleanly | **Strong** — skills/agents/hooks work natively |
| **Reliability / stability** | Moderate — latency, cache staleness, Windows path issues | Weak — not in registry, known crashes, silent failures | **Strong** — direct I/O, git safety, proven at 15M words |
| **Plugin ecosystem access** | **Strong** — Templater, Smart Connections, Dataview, Graph | **Strong** — full sidebar UI, can also connect to MCP | Weak — no Obsidian plugin access |
| **Batch processing / scale** | Weak — token exhaustion at 3000+ notes, 10min cache | Weak — API costs scale linearly, no batch optimization | **Strong** — Grep/Glob handle thousands of files in seconds |

#### Recommendation

**Direct Filesystem (primary) + MCP Servers (supplemental).**

Build commandbase-vault skills around direct filesystem access as the foundation. This leverages the existing skill system without abstraction layers, ensures git-backed safety for bulk operations, and scales reliably on Windows. Use the already-configured obsidian-mcp-tools as a supplemental layer for narrow cases where semantic search or Templater execution are needed — invoke via ToolSearch when skills explicitly require Smart Connections or template rendering. Embedded plugins are not recommended due to instability, lack of official Obsidian approval, and duplication of commandbase functionality.

## Source Conflicts

**MCP vs. Filesystem access:** Some sources advocate MCP servers for structured tool access, while others (Eleanor Konik, Kyle Gao) prefer direct Claude Code filesystem access for simplicity. Both approaches work; MCP adds semantic search and Templater integration at the cost of complexity.

**Flat vs. hierarchical structure:** Steph Ango (Obsidian CEO) advocates near-flat vaults with minimal folders, while the AI-native community favors numeric-prefixed categorical folders. The compromise is shallow hierarchy (1-2 levels) with aggressive linking.

**Automation level:** Forum consensus is cautious ("exploratory tool, not permanent workflow"), while power users like Eleanor Konik run overnight batch processing on 15M-word vaults. The gap is experience and git safety nets.

**Cloud vs. local AI:** Tension between cloud API convenience and local model privacy. PrivateAI plugin, Time Garden, and local LLM setups are growing but less capable than Claude.

**Centralized vs. in-note storage:** True Recall uses SQLite (Anki-style) for flashcards; SRAI embeds cards in notes. Both approaches have trade-offs for portability vs. integration.

## Currency Assessment
- Most recent source: February 2026 (mcp-obsidian-advanced, Agent Client plugin)
- Topic velocity: Fast-moving (new plugins and patterns monthly)
- Confidence in currency: High for integration options, medium for best practices (still evolving)

## Open Questions
- How does CLAUDE.md length affect token consumption and session performance?
- What's the optimal vault size threshold before semantic search outperforms keyword search?
- How to handle multi-vault configurations (personal/work separation) with shared CLAUDE.md patterns?
- When will Claude Code support the 2025-03-26 Streamable HTTP MCP protocol?
- What are the best practices for mobile vault access with AI integration? (Currently desktop-only)
