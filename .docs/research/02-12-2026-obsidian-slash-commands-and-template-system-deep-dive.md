---
date: 2026-02-12
status: complete
topic: "Obsidian Slash Commands & Template System Deep Dive"
tags: [research, obsidian, claude-code, slash-commands, templates, templater, automation, vault-management]
git_commit: 9c4c7f4
---

# Obsidian Slash Commands & Template System Deep Dive

## Research Question
What are the full capabilities, best practices, and creative patterns for slash commands and template systems when managing an Obsidian vault with Claude Code?

## Summary
The Obsidian vault automation landscape offers three complementary templating layers: **Claude Code slash commands/skills** (`.claude/commands/` and `.claude/skills/`), **Obsidian Templater** (JavaScript-powered dynamic templates), and **AI-powered template plugins** (Smart Templates, QuickAdd AI Assistant, Text Generator). Claude Code commands have evolved into the Agent Skills open standard, supporting frontmatter controls, argument passing, inline bash substitution, and progressive disclosure. Templater provides the most powerful in-Obsidian template engine with full JavaScript execution, system commands, and MCP integration via obsidian-mcp-tools. Community repos like kepano/obsidian-skills (official, 5 skills), ashish141199/obsidian-claude-code (9 commands), ZanderRuss/obsidian-claude (29 commands, 16 agents), and ballred/obsidian-claude-pkm (complete PKM kit) demonstrate mature patterns. The optimal approach for commandbase-vault is direct filesystem skills augmented by MCP for Templater execution when needed.

## Detailed Findings

### 1. Claude Code Slash Commands & Skills

**Sources:** [Claude Code Skills Docs](https://code.claude.com/docs/en/skills), [Agent Skills Specification](https://agentskills.io/specification), [AI Engineering Report](https://www.aiengineering.report/p/claude-code-custom-commands-3-practical)

#### File Format & Location
- **Project commands**: `.claude/commands/<name>.md` — available in current project only
- **Personal commands**: `~/.claude/commands/<name>.md` — available across all projects
- **Skills**: `.claude/skills/<name>/SKILL.md` — directory-based with supporting files
- Filename becomes command name: `commit.md` → `/commit`
- Subdirectories create namespaces: `.claude/commands/posts/new.md` → `/posts:new`

#### Frontmatter Controls
```yaml
---
name: fix-issue
description: Fix a GitHub issue
argument-hint: [issue-number]
allowed-tools: Bash(git *)
disable-model-invocation: true
user-invocable: true
model: sonnet
context: fork
agent: Explore
---
```

Key fields:
- `name` — Command name (lowercase, hyphens, max 64 chars)
- `description` — Max 1024 chars; helps Claude decide when to auto-invoke
- `argument-hint` — Autocomplete hints for arguments
- `disable-model-invocation: true` — Prevents Claude from auto-invoking (manual only)
- `user-invocable: false` — Hides from `/` menu (background knowledge only)
- `allowed-tools` — Pre-approved tools (e.g., `Bash(git *)`, `Read`, `Grep`)
- `context: fork` — Run in isolated subagent context
- `agent` — Subagent type (`Explore`, `Plan`, `general-purpose`)

#### Argument Handling
- `$ARGUMENTS` — All arguments passed after command name
- `$ARGUMENTS[N]` or `$N` — Access specific argument by index (0-based)
- `${CLAUDE_SESSION_ID}` — Current session ID
- If a skill doesn't include `$ARGUMENTS`, Claude Code automatically appends `ARGUMENTS: <input>` to the end

#### Inline Bash Substitution
The `` !`command` `` syntax executes shell commands **before** the skill content is sent to Claude, replacing the placeholder with actual output:
```markdown
## PR Context
- PR diff: !`gh pr diff`
- Changed files: !`gh pr diff --name-only`
```
This is preprocessing — Claude receives the fully-rendered prompt with real data.

#### Commands vs Skills Decision Matrix

| Aspect | Slash Commands | Skills |
|--------|----------------|--------|
| Invocation | Manual only (`/command`) | Manual OR automatic (Claude detects relevance) |
| Context loading | Full content inserted every time | Description only until invoked (lazy-loading) |
| File structure | Single `.md` file | Directory with `SKILL.md` + supporting files |
| Supporting files | None | Can include `scripts/`, `references/`, `assets/` |
| Best for | Repeatable workflows with side effects | Background knowledge, complex multi-file workflows |

**Best Practice**: Start with a command. Migrate to a skill when you need supporting files or auto-invocation.

#### Agent Skills Open Standard
Claude Code skills follow the [Agent Skills](https://agentskills.io) open standard (works across Claude Code, Codex CLI, etc.):
```
skill-name/
├── SKILL.md           # Required: YAML frontmatter + Markdown instructions
├── scripts/           # Optional: Executable code
├── references/        # Optional: Additional docs loaded on demand
└── assets/            # Optional: Templates, images, data files
```

Progressive disclosure model:
1. **Metadata** (~100 tokens): `name` + `description` loaded at startup for all skills
2. **Instructions** (< 5000 tokens recommended): Full `SKILL.md` body loaded when activated
3. **Resources** (as needed): Files in subdirectories loaded only when required

### 2. Obsidian Templater Plugin

**Sources:** [Templater Docs](https://silentvoid13.github.io/Templater/introduction.html), [GitHub](https://github.com/SilentVoid13/Templater), [Nicole van der Hoeven](https://nicolevanderhoeven.com/blog/20220131-5-things-the-obsidian-templater-can-do-that-templates-cant/)

#### Core Capabilities
- Full JavaScript execution within templates
- System command execution with output capture
- Dynamic variables: file metadata, dates, frontmatter, user input
- User scripts: custom CommonJS modules via `tp.user.<script>()`
- Template chaining via `tp.file.include()`
- Hooks system for post-template-execution code
- Web requests: fetch content, random images, daily quotes

#### Syntax Reference
```
<%  expression %>     — Interpolation (outputs result)
<%* code %>           — Execution (runs JS, no auto-output; use tR += "text")
<%_ ... %>            — Trim all whitespace before
<% ... _%>            — Trim all whitespace after
<%- ... %>            — Trim one newline before
<% ... -%>            — Trim one newline after
```

#### Key Module Functions

**tp.file** — File operations:
- `tp.file.title` — Filename without extension
- `tp.file.creation_date("YYYY-MM-DD")` — Creation timestamp
- `tp.file.create_new(template, filename, open, folder)` — Create files from templates
- `tp.file.include([[Note]])` — Include file content (supports sections/blocks)
- `tp.file.move(new_path)` — Move/rename file
- `tp.file.exists(filepath)` — Check file existence
- `tp.file.tags` — Array of file tags

**tp.date** — Date operations (Moment.js formatting):
- `tp.date.now("YYYY-MM-DD", 7)` — Current date + 7 day offset
- `tp.date.tomorrow()`, `tp.date.yesterday()`
- `tp.date.weekday("dddd", 1)` — Specific weekday

**tp.system** — User interaction:
- `tp.system.prompt("Question?")` — Text input modal
- `tp.system.suggester(["A","B"], [1,2])` — Selection menu
- `tp.system.clipboard()` — Get clipboard content

**tp.web** — Web requests:
- `tp.web.request(url, path?)` — HTTP request with optional JSON path
- `tp.web.daily_quote()` — Fetch daily quote callout
- `tp.web.random_picture(size, query)` — Random Unsplash image

**tp.frontmatter** — YAML frontmatter access:
- `tp.frontmatter.<variable_name>` or `tp.frontmatter["variable name"]`

#### User Scripts
- Create `.js` files in designated scripts folder
- Export CommonJS modules: `module.exports = function(tp) { ... }`
- Access via `tp.user.<script_name>(tp)` — must pass `tp` as argument
- Can access global namespace: `app`, `moment`

#### System Commands
- Define function name → shell command in settings
- Pass arguments as JS object: `tp.user.echo({a: "value1", b: "value2"})`
- Arguments become environment variables (`$a`, `$b` in bash)
- Can embed internal functions: `cat <% tp.file.path() %>`

#### Folder & File Regex Templates
- Auto-apply templates to specific folders (deepest match wins)
- Regex-match new file paths (first match applies)
- **Mutually exclusive** — can't use both simultaneously
- Startup templates execute once on Templater init (no output)

#### Templater vs Core Templates
Core templates: basic date/time insertion, static content, works in Restricted Mode.
Templater adds: dynamic variables, context-sensitive templates, JavaScript execution, plugin integration, auto-incrementing, conditional logic. Quote: "What the core Templates plugin should have been" — Nicole van der Hoeven.

**Trade-off**: Requires disabling Restricted Mode; steeper learning curve.

#### MCP Integration
obsidian-mcp-tools provides `execute_template` tool for running Templater templates remotely:
- Requires Obsidian running + Local REST API plugin + Templater plugin
- Claude/MCP client sends template name + parameters
- Templater executes within Obsidian environment
- Results returned to MCP client

#### Limitations & Gotchas
- **Security**: Arbitrary JS and system command execution — only run trusted code
- **Folder/Regex mutual exclusivity**: Can't enable both template types simultaneously
- **tp.frontmatter**: May not work reliably on file creation (Issue #1290)
- **Web module**: Templates fail if internet unavailable when using `tp.web.*`
- **Duplicate prompts**: May trigger multiple times from templates (reported bug)

### 3. AI-Powered Template Plugins

**Sources:** [Smart Templates GitHub](https://github.com/brianpetro/obsidian-smart-templates), [QuickAdd AI Docs](https://quickadd.obsidian.guide/docs/AIAssistant/), [Text Generator GitHub](https://github.com/nhaouari/obsidian-textgenerator-plugin)

#### Smart Templates (brianpetro)
- Privacy-first AI content generation with local/cloud model support
- EJS syntax for template logic and variable substitution
- Smart Context integration for dynamic context injection
- Supports Ollama, LM Studio, Claude, Gemini, OpenAI
- Core (free): prompt builder + clipboard workflow; Pro: modal previews, AI prompts, multiple output targets

#### QuickAdd AI Assistant
- **Prompt chaining**: "Multiple prompts chained together with each using the output of the previous one"
- Implementation: Stack AI Assistant in a QuickAdd Macro; each step uses `{{value}}` to reference previous output
- Supports OpenAI-compatible APIs, Google Gemini, Ollama
- Four core tools: Templates, Captures, Macros, Multis
- Full JavaScript API for custom automation

#### Text Generator
- Versatile AI content generation with template engine
- Community template sharing and discovery
- Supports OpenAI, Claude, Gemini, HuggingFace, local models
- Free and open source — "the standard for writing and drafting"
- Frontmatter-based prompt configuration

#### Smart Composer
- Cursor-like editing for Obsidian with RAG semantic search
- Prompt templates via `/` command in chat input
- One-click apply for AI-suggested edits
- Supports OpenAI, Claude, Gemini, Groq, Ollama

#### Nova
- AI writing assistant that edits directly in-note (no chat window)
- Smart fill: comment placeholders throughout document, generate all at once
- Privacy core: local AI via Ollama/LM Studio, or bring your own API keys
- Zero telemetry; AGPL-3.0 license

#### Plugin Comparison

| Plugin | Primary Use | Multi-Step | Local Models | Template System | Stars |
|--------|------------|-----------|-------------|----------------|-------|
| Copilot | Chat sidebar | Limited | Ollama | Slash commands | 5,776 |
| Smart Connections | Semantic search | Via context | 100+ models | No | 4,357 |
| Text Generator | Writing/drafting | Via templates | Yes | Frontmatter engine | 1,837 |
| Smart Templates | AI generation | Via context | Ollama | EJS + frontmatter | — |
| QuickAdd | Workflow automation | Prompt chains | Ollama | Format syntax | — |
| Smart Composer | Cursor-like editing | Via RAG | Ollama | Prompt templates | — |
| Nova | In-note editing | Smart fill | Ollama, LM Studio | Comment placeholders | — |
| Claudian | Full agentic | Multi-step agents | No (Claude only) | Slash command files | — |

### 4. Community Vault Command Repos

**Sources:** [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills), [ashish141199/obsidian-claude-code](https://github.com/ashish141199/obsidian-claude-code), [ZanderRuss/obsidian-claude](https://github.com/ZanderRuss/obsidian-claude), [ballred/obsidian-claude-pkm](https://github.com/ballred/obsidian-claude-pkm)

#### kepano/obsidian-skills (Official, by Obsidian CEO)
5 skills following Agent Skills specification:
1. **obsidian-markdown** — Obsidian Flavored Markdown (wikilinks, embeds, callouts, properties)
2. **obsidian-bases** — Obsidian Bases (.base files with views, filters, formulas)
3. **json-canvas** — JSON Canvas (.canvas with nodes, edges, groups)
4. **obsidian-cli** — Vault interaction via Obsidian CLI
5. **defuddle** — Clean markdown extraction from web pages

Key insight: "Without strict guidance, AI tends to bungle field names, nesting, or structure. The skill keeps it on the rails."

#### ashish141199/obsidian-claude-code (9 commands)
| Command | Function |
|---------|----------|
| `/day` | Interactive daily journaling with smart linking |
| `/new` | Create atomic topic notes |
| `/research` | Web search and synthesize findings |
| `/brainstorm` | Generate ideas using vault connections |
| `/log` | Quick logging without conversation |
| `/answer` | Query vault knowledge base |
| `/task` | Task management in todo.md |
| `/save` | Git commit and push automation |
| `/resource` | Capture articles/videos as linked notes |

Design principles: Link Everything, Atomic Notes, Graph-First, Concise Writing.

#### ZanderRuss/obsidian-claude (29 commands, 16 agents)
Most comprehensive repo. Categories:
- **Knowledge workflows** (5): `/thinking-partner`, `/daily-review`, `/weekly-synthesis`, `/research-assistant`, `/inbox-processor`
- **Advanced analysis** (4): `/smart-link`, `/graph-analysis`, `/extract-todos`, `/summarize-project`
- **Content transformation** (4): `/flashcards`, `/note-to-blog`, `/voice-process`, `/web-clip`
- **Academic research** (11): `/research-ideate`, `/quick-research`, `/deep-research`, `/lit-search`, `/lit-review`, `/paper-outline`, `/paper-draft`, `/paper-review`, etc.
- **16 agents**: vault-optimizer, moc-agent, tag-agent, content-curator, metadata-agent, connection-agent, review-agent, prompt-engineer, search-specialist, task-decomposition-expert, plus 6 research team agents
- **3-layer quality control**: Prevention → Detection → Validation (≥0.8 score required)

#### ballred/obsidian-claude-pkm (Complete PKM Kit v2.1)
- Commands: `/daily`, `/weekly`, `/push`, `/onboard`
- 4 agents: Note Organizer, Weekly Reviewer, Goal Aligner, Inbox Processor
- Hooks: session init, auto-commit
- Rules: path-specific markdown/productivity conventions
- Output styles: "Productivity Coach" persona

#### aplaceforallmystuff/daily-patterns-pack
- `/log-to-daily` — captures Claude Code sessions as structured daily note entries
- `@vault-analyst` agent — analyzes accumulated dailies to find automation opportunities
- Compounding effect: better logs → better pattern detection → better automation → better logs

### 5. Creative Automation Patterns

**Sources:** Multiple repos and blog posts

#### Daily Note Architecture
- `/day` or `/daily` creates/opens today's note with smart linking
- `/mise-en-place` (curiouslychase): Run Bun setup script → Review North Star → Prepare weekly check-ins
- `/top-3` establishes daily priorities
- Evening `/wrapup` or `/daily-review` with auto-commit

#### Weekly Review Pattern
Reflect → Connect → Plan (60-90 min block):
- `/weekly-synthesis` identifies patterns across daily notes
- Automatic rollup from daily → weekly → monthly → quarterly notes
- Dataview queries auto-maintain aggregations

#### Backlinking Automation
"Read my journal entry and add backlinks to all people, places, and books mentioned. Search vault for existing entity notes, create new ones if needed." — 15 seconds vs 10-15 minutes manual.

#### Inbox Processing
- PARA-based classification: `/inbox-processor`
- QuickAdd capture for rapid input
- Dataview query shows unsorted files; files auto-leave inbox when linked

#### MOC Auto-Generation
- Python script (`generate_mocs.py`) creates `_MOC.md` per folder with all links
- Dataview queries: `LIST FROM #tagname`
- AI-powered topic modeling suggests groupings
- `/find-connections` discovers non-obvious relationships

#### Content Transformation
- `/flashcards` — Spaced repetition card generation
- `/note-to-blog` — Transform notes into publishable content
- `/voice-process` — Structure voice transcriptions
- `/web-clip` or `/digest` — Save web articles as structured markdown

#### CI/CD Pipeline Integration
GitHub Actions for vault automation:
- Lint and link validation on every push
- Scheduled daily health checks
- Multi-format export (HTML, PDF)
- Knowledge graph generation
- AI enhancement commands: `ai:summarize`, `ai:tag`, `ai:connect`
- Auto-create GitHub issues when health checks fail

### 6. Prompt Engineering Patterns for Vault Commands

**Sources:** [builder.io](https://www.builder.io/blog/claude-code), [htdocs.dev](https://htdocs.dev/posts/claude-code-best-practices-and-pro-tips/), [curiouslychase](https://www.curiouslychase.com/posts/ai-native-obsidian-vault-setup-guide)

#### Writing Effective Commands
1. **Be selective**: Use commands for long prompts you frequently repeat
2. **Use arguments**: Always include `$ARGUMENTS` with `argument-hint` for autocomplete
3. **Include guardrails**: "Read the actual error before proposing fixes", "Only report bugs, be concise"
4. **Number steps explicitly**: 1, 2, 3... for clear execution order
5. **Reference conventions**: Point to style guides, API docs, CLAUDE.md rules
6. **Namespace with subdirectories**: `posts/new.md` → `/posts:new`
7. **Keep SKILL.md under 500 lines**: Move details to `references/`
8. **Control invocation**: `disable-model-invocation: true` for side-effect workflows

#### CLAUDE.md as Vault Constitution
Essential sections for vault management:
- Vault purpose and personal context
- Folder structure with explanations
- File naming conventions
- Tagging taxonomy rules
- Linking conventions (wikilinks, when to create new notes)
- Frontmatter schema (required/optional properties per note type)
- Tone preferences
- Forbidden actions

#### Error Documentation Pattern
Create a file logging corrections and solutions so Claude learns from mistakes. When correcting Claude, tell it to write the fix to CLAUDE.md.

### 7. Integration Architecture for commandbase-vault

**Sources:** Cross-referenced from all agents

#### Recommended Three-Layer Approach

**Layer 1: Direct Filesystem (Primary)**
- Claude Code skills read/write markdown files directly
- Grep/Glob for vault search (handles thousands of files in seconds)
- Git-backed safety for all modifications
- Same skill/agent/hook system as all commandbase plugins
- Proven at scale: Eleanor Konik processed 15M-word vault overnight

**Layer 2: Obsidian MCP (Supplemental)**
- Use obsidian-mcp-tools via ToolSearch for:
  - Semantic search (Smart Connections embeddings)
  - Templater template execution
  - Plugin-specific operations
- Only invoke when skills explicitly need these capabilities
- Already configured in user's environment

**Layer 3: kepano/obsidian-skills (Reference Knowledge)**
- Install obsidian-skills for Obsidian-specific format knowledge
- Provides Claude with correct wikilink, callout, properties, Bases, Canvas syntax
- Prevents AI from "bungling field names, nesting, or structure"

## Source Conflicts

**Commands vs Skills terminology**: Some sources treat these as distinct systems; the official docs confirm they're now unified — both create slash commands, with skills adding optional features (supporting files, auto-invocation, progressive disclosure).

**Templater vs direct filesystem**: MCP integration for Templater execution requires Obsidian running + Local REST API + Templater plugins. Direct filesystem approach works without Obsidian running but can't execute Templater templates or access semantic search. Both valid; choice depends on whether Templater features are needed.

**QuickAdd vs Smart Templates vs Text Generator**: All three provide AI template capabilities with overlapping feature sets. Community consensus: QuickAdd for workflow automation + AI chaining, Text Generator for writing/drafting (free, standard), Smart Templates for privacy-first AI generation. They serve different primary use cases.

**Template complexity**: Some repos (ZanderRuss: 29 commands, 16 agents) demonstrate sophisticated systems, while experts like Eleanor Konik recommend starting simple and growing organically. The curiouslychase approach (numeric-prefix structure + focused commands) represents a middle ground.

## Currency Assessment
- Most recent sources: February 2026 (kepano/obsidian-skills, Nova plugin, obsidian-mcp-tools updates)
- Topic velocity: Very fast-moving (new plugins and repos weekly)
- Confidence in currency: High for Claude Code command format (stable API), medium for plugin ecosystem (rapid churn)
- Agent Skills specification appears stable; community adoption growing

## Open Questions
- How do Claude Code skills perform at scale with large vaults (10K+ notes) where `$ARGUMENTS` includes vault-wide context?
- What's the token impact of progressive disclosure for skills vs. commands in practice?
- Can Templater user scripts be triggered from Claude Code without MCP (e.g., via obsidian:// URI scheme)?
- How to handle template execution when Obsidian is not running (common in terminal-only workflows)?
- What's the optimal split between Claude Code skills and Templater templates for vault automation?
- When will the Agent Skills specification support template variable passing natively?
