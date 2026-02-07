---
date_researched: 2026-02-06
sources: [context7]
primary_framework: "Claude Code CLI (skills, agents, hooks)"
status: current
---

# Framework Documentation Snapshot

Research date: 2026-02-06
Sources: Context7 MCP (6 libraries queried)
Shelf life: Review after 60 days (Claude Code updates frequently)

## Claude Code Skills Specification (Tier 1)

### Source
- `/llmstxt/code_claude_llms_txt` (Trust: 9.9, 1659 snippets)
- `/anthropics/skills` (Trust: 8.5, 886 snippets)

### Skill File Format
- File: `SKILL.md` in skill directory
- Location: `~/.claude/skills/<skill-name>/SKILL.md` (global) or `.claude/skills/<skill-name>/SKILL.md` (project)
- Required frontmatter: `name` (kebab-case), `description` (invocation-focused)
- Optional frontmatter: `context: fork`, `agent: Explore`, `disable-model-invocation: true`, `user-invocable`, `allowed-tools`, `model`, `argument-hint`, `hooks`
- **NOTE (2026-02-06 correction):** `skills` is NOT valid SKILL.md frontmatter — it only works in agent `.md` files. Original Context7 research incorrectly conflated agent and skill frontmatter.

### Key Features
- **`$ARGUMENTS`**: Substituted with user-provided arguments after skill invocation
- **`context: fork`**: Runs skill in isolated context (subagent), preventing context pollution
- **`skills` preloading**: Load other skills as dependencies — **agent frontmatter only** (not valid in SKILL.md)
- **`hooks` in frontmatter**: Attach hooks that only activate when the skill is running
- **`allowed-tools`**: Restrict which tools the skill can use
- **`disable-model-invocation: true`**: Prevent the skill from being auto-invoked by the model
- **Progressive disclosure**: Body (SKILL.md) + `reference/` dir + `templates/` dir

### Skill Description Formula
```
"Use this skill when [trigger conditions]. This includes [2-3 specific actions]. Activate when the user says [3-4 trigger phrases]."
```

### Naming Convention
- Gerund form (present participle): `researching-frameworks`, `creating-skills`
- Kebab-case, lowercase: `^[a-z][a-z0-9-]*$`

---

## Claude Code Hooks API (Tier 1)

### Source
- `/llmstxt/code_claude_llms_txt` (Trust: 9.9)
- `/mizunashi-mana/claude-code-hook-sdk` (Trust: 9.0, 80 snippets)

### Hook Events (7 types)
| Event | When | Can Block? |
|-------|------|-----------|
| PreToolUse | Before tool execution | Yes (approve/block) |
| PostToolUse | After tool completes | Yes (block) |
| Notification | System notification | No |
| Stop | Main agent stopping | Yes (block) |
| SubagentStop | Subagent stopping | Yes (block) |
| UserPromptSubmit | User submits prompt | Yes (block) |
| PreCompact | Before context compaction | No |

### Hook Input (stdin JSON)
```typescript
interface BaseHookInput {
  session_id: string;
  transcript_path: string;
  hook_event_name: string;
}

// PreToolUse adds: tool_name, tool_input
// PostToolUse adds: tool_name, tool_input, tool_response
// Stop/SubagentStop adds: stop_hook_active
// UserPromptSubmit adds: prompt
// PreCompact adds: trigger, custom_instructions
// Notification adds: message
```

### Hook Output (stdout JSON)
```typescript
interface PreToolUseOutput {
  decision?: 'approve' | 'block';
  reason?: string;
}

interface PostToolUseOutput {
  decision?: 'block';
  reason?: string;
}
// Stop, SubagentStop, UserPromptSubmit also support block decisions
```

### Configuration (settings.json)
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "python script.py" }
        ]
      }
    ]
  }
}
```

### Matcher Patterns
- `"*"` — matches all tools
- `"Bash"` — matches specific tool
- `"Edit|Write|MultiEdit"` — matches multiple tools (pipe-separated)
- `"Notebook.*"` — regex pattern

---

## Claude Code Agents/Subagents (Tier 1)

### Source
- `/llmstxt/code_claude_llms_txt` (Trust: 9.9)
- `/davepoon/claude-code-subagents-collection` (Trust: 9.5, 915 snippets)

### Agent File Format
- File: `<agent-name>.md` in agents directory
- Location: `~/.claude/agents/` (global) or `.claude/agents/` (project)
- Required frontmatter: `name`, `description`
- Optional frontmatter: `tools`, `model`, `category`, `color`

### Agent Frontmatter
```yaml
---
name: backend-architect
description: Design RESTful APIs, microservice boundaries, and database schemas. Use PROACTIVELY when creating new backend services.
tools: Read, Write, Edit, Bash
model: sonnet
---
```

### Agent Body Structure
1. Role statement ("You are a...")
2. "When invoked:" numbered steps
3. "Process:" bullet points
4. "Provide:" deliverables list

### Invocation
- Spawned via Task tool with `subagent_type` parameter
- Can be invoked explicitly: `@agent-name help me with X`
- Can be triggered proactively based on description keywords

---

## Hook SDK — TypeScript (Tier 2)

### Source
- `/mizunashi-mana/claude-code-hook-sdk` (Trust: 9.0, 80 snippets)

### Package
```bash
npm install -D @mizunashi_mana/claude-code-hook-sdk tsx
```

### Core API
- **`runHook(handlers)`** — Main entry point, reads stdin JSON, routes to handlers
- **`parseHookInput(json)`** — Validates input with Zod schemas
- **`isKnownHookInput(input, event)`** — Type guard for event discrimination
- **`execFileAsync(cmd, args)`** — Async wrapper for child_process.execFile

### Utility Hooks
- **`preToolRejectHook(config)`** — Block Bash commands by regex/function patterns
- **`postToolUpdateFileHook(handler)`** — Process file modifications from Write/Edit/MultiEdit
- **`runHookCaller(handler, input)`** — Programmatic hook testing

### Settings Configuration
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "npx tsx hooks/my-hook.ts" }
        ]
      }
    ]
  }
}
```

### Key Advantage Over Raw Python
- Full TypeScript types for all 7 event inputs/outputs
- Zod runtime validation catches malformed input
- `preToolRejectHook` eliminates boilerplate for command blocking
- `postToolUpdateFileHook` extracts file paths, added/deleted lines automatically
- `runHookCaller` enables unit testing hooks without Claude Code running

---

## Community Templates (Tier 3)

### Source
- `/davila7/claude-code-templates` (Trust: 10, 2306 snippets)

### Overview
CLI tool for installing pre-built Claude Code components:
```bash
npx claude-code-templates@latest --agent=react-performance --yes
npx claude-code-templates@latest --hook=git-workflow/auto-git-add
npx claude-code-templates@latest --command=generate-tests
```

### Component Types
- Agents (expert-advisors, programming-languages, development-tools)
- Commands (slash commands with frontmatter)
- Hooks (git-workflow, automation, security, development-tools, performance)
- MCPs (service integrations)
- Settings (model preferences, timeouts)

### Relevance to Commandbase
- Reference for agent/hook patterns used in the community
- Not a dependency — our skills are more structured than their templates
- Hook categories (git-workflow, security, development-tools) mirror our use cases

---

## Subagents Collection (Tier 3)

### Source
- `/davepoon/claude-code-subagents-collection` (Trust: 9.5, 915 snippets)

### Overview
Curated collection of agent `.md` files organized by category:
- development-architecture
- language-specialists
- infrastructure-operations
- quality-security
- data-ai
- specialized-domains

### Installation
```bash
# Global
cp subagents/*.md ~/.claude/agents/

# Project-local
mkdir -p .claude/agents
cp subagents/*.md .claude/agents/
```

### BWC CLI
A separate CLI tool (`bwc`) for managing agents and commands with scope awareness (project vs user-level).
