# Tool Selection Guide

Tool selection is a security and focus decision. Every tool an agent has is a tool it could misuse. Start from deny-all and add only what the workflow requires.

## The Principle

> "Permission sprawl is the fastest path to unsafe autonomy. Treat tool access like production IAM. Start from deny-all; allowlist only what a subagent needs."

## Tools vs DisallowedTools

| Field | What It Does | When to Use |
|-------|-------------|-------------|
| `tools` | Allowlist - agent can ONLY use these tools | Agent needs a small, specific set |
| `disallowedTools` | Denylist - agent gets all tools EXCEPT these | Agent needs most tools but a few are dangerous |
| Neither (omit both) | Inherits all parent tools | Only when agent truly needs everything |

**Default choice**: Use `tools` (allowlist). It's safer and more explicit.

**Don't use both** on the same agent - they're mutually exclusive approaches.

## Common Tool Sets by Agent Type

### Locator Agents (find where things are)

```yaml
tools: Grep, Glob, LS
```

No `Read` - locators find paths, they don't analyze content. This constraint keeps them fast and focused.

### Analyzer Agents (understand how things work)

```yaml
tools: Read, Grep, Glob, LS
```

Adds `Read` for content analysis. No modification tools - analyzers report, they don't change.

### Pattern Finder Agents (find similar code)

```yaml
tools: Grep, Glob, Read, LS
```

Same as analyzer but the Read tool is essential for extracting code snippets to show as examples.

### Research Agents (gather external information)

```yaml
tools: WebSearch, WebFetch
```

Specialized external tools only. No file system access needed for pure web research.

### Updater/Builder Agents (modify state)

```yaml
tools: Read, Grep, Glob, LS, Edit, Bash
```

**Caution**: These agents can change things. Must have:
- Explicit decision framework in system prompt
- "What NOT to Do" enforcement
- Conservative defaults ("when uncertain, don't modify")
- Consider `model: opus` for better judgment

### Review Agents (evaluate quality)

```yaml
tools: Read, Grep, Glob, LS
```

Read access for thorough analysis, no modification access. Reviews should be advisory.

## Decision Framework

For each tool, ask:

1. **Does the workflow require this tool?** Map each step of the agent's process to the tools it needs.
2. **What could go wrong?** Consider what happens if the agent misuses this tool.
3. **Is there a safer alternative?** Can the agent accomplish the same goal with a more constrained tool?

### Tool Risk Levels

| Risk | Tools | Requires |
|------|-------|----------|
| **Low** (read-only) | Glob, Grep, LS, Read, WebSearch, WebFetch | Minimal guardrails |
| **Medium** (content modification) | Edit, Write, NotebookEdit | Decision framework + enforcement |
| **High** (arbitrary execution) | Bash, Task | Extensive guardrails, consider `opus` model |

## State Modification Guardrails

If an agent needs Edit, Write, or Bash, add these to the system prompt:

1. **Decision tree**: Explicit conditions for when to modify vs. when to skip
2. **Conservative default**: "When uncertain, do not modify"
3. **What NOT to Do**: Specific dangerous actions that are off-limits
4. **Verification**: Agent should verify its changes after making them

Example pattern:
```markdown
## Decision Framework

**Modify if:**
- [Explicit condition 1]
- [Explicit condition 2]

**Do NOT modify if:**
- [Explicit condition 1]
- [Explicit condition 2]

**When uncertain: do not modify. Report findings instead.**
```

## Special Tool Considerations

### Task Tool

Giving an agent the `Task` tool means it can spawn sub-agents of its own. This creates agent hierarchies. Only do this for orchestrator-level agents that genuinely need to delegate.

### Bash Tool

The most powerful and dangerous tool. An agent with Bash can run arbitrary commands. Reserve for agents that genuinely need to execute commands (build tools, deployment, system operations). Always pair with explicit command restrictions in the system prompt.

### WebFetch / WebSearch

Only needed for agents that must access external information. Most codebase-focused agents don't need these.

## Red Flags

- Agent has no `tools` field and inherits everything -> Add explicit tool list
- Agent has Edit but its system prompt never mentions file modification -> Remove Edit
- Agent has Bash but only uses it for `grep` or `find` -> Replace with Grep and Glob tools
- Agent has WebSearch but never needs external information -> Remove WebSearch
- Two agents in the same family have identical tool sets but different roles -> Verify they genuinely need the same tools
