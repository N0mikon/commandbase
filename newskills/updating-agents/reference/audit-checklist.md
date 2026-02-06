# Audit Checklist

Complete checklist for agent validation. Each item maps to the agent specification rules at `~/.claude/skills/creating-agents/reference/validation-rules.md`.

## 1. Frontmatter Checks

| Check | Pass Condition |
|-------|----------------|
| Opens with delimiter | First line is exactly `---` |
| Closes with delimiter | Frontmatter ends with `---` on own line |
| Valid YAML | Content parses as YAML without errors |
| Is dictionary | Parsed YAML is object, not array or scalar |
| Allowed properties only | Only: name, description, tools, disallowedTools, model, permissionMode, skills, hooks, memory |
| Has name | `name` field present and non-empty |
| Has description | `description` field present and non-empty |
| No unknown properties | Flag any property not in the allowed list (may be typo) |

## 2. Name Checks

| Check | Pass Condition |
|-------|----------------|
| Valid format | Matches `^[a-z0-9-]+$` |
| No leading hyphen | Does not start with `-` |
| No trailing hyphen | Does not end with `-` |
| No consecutive hyphens | Does not contain `--` |
| Length limit | 64 characters or fewer |
| Matches filename | Name equals filename minus `.md` extension exactly |
| Noun/role form | Does NOT use gerund (verb-ing) pattern |
| No vague suffix | Does not end in `-helper`, `-handler`, `-manager`, `-util` |

**Gerund detection heuristic:** Flag if the name contains a component ending in `-ing` that is the verb portion. Examples:
- `code-analyzer` OK (analyzer is a noun/role)
- `code-reviewing` BAD (reviewing is a gerund - skill pattern)
- `code-librarian` OK (finder is a noun/role)
- `finding-patterns` BAD (finding is a gerund)

**Note:** Some words ending in `-ing` are legitimate nouns (e.g., `testing` as a domain). Use judgment - the test is whether the name describes WHAT the agent IS (noun) vs WHAT ACTION it performs (gerund).

## 3. Description Checks

| Check | Pass Condition |
|-------|----------------|
| Non-empty | After trim, length > 0 |
| Is string | Type is string |
| Length limit | 1024 characters or fewer |
| No angle brackets | Does not contain `<` or `>` |
| Not first person | No "I help", "I am", "I will", "My purpose" |
| Has delegation trigger | Contains language indicating when to delegate (e.g., "Call when", "Use when", "when you need to") |
| Not skill-style | Does NOT start with "Use this skill when" |
| Distinguishable | Description does not substantially overlap with other agents |

**First person detection:** Flag if description contains:
- "I help"
- "I am"
- "I will"
- "I can"
- "My purpose"
- "This agent helps you" (second person addressing)

**Delegation trigger detection:** Description should contain at least one indicator:
- "when you need to..."
- "Call this agent when..."
- "Use when..."
- An imperative delegation context in the second sentence

## 4. Tool Set Checks

| Check | Pass Condition |
|-------|----------------|
| No mutual exclusivity | `tools` and `disallowedTools` are NOT both present |
| tools is array | If present, `tools` is an array of strings |
| disallowedTools is array | If present, `disallowedTools` is an array of strings |
| Valid tool names | All listed tools are recognized tool names |
| Explicit tool set | Either `tools` or `disallowedTools` is specified (not relying on inherit-all) |
| Edit guardrails | If `Edit` in tools, system prompt has modification guardrails |
| Write guardrails | If `Write` in tools, system prompt has creation guardrails |
| Bash guardrails | If `Bash` in tools, system prompt has command restrictions |
| NotebookEdit guardrails | If `NotebookEdit` in tools, system prompt has notebook guardrails |
| No unnecessary WebSearch | If `WebSearch` in tools, agent's purpose involves external information |
| No unnecessary Bash | If `Bash` in tools, purpose requires command execution (not just grep/find) |
| Task tool justified | If `Task` in tools, agent is orchestrator-type |

**Known valid tool names:** Read, Write, Edit, Bash, Glob, Grep, LS, WebSearch, WebFetch, Task, NotebookEdit, NotebookRead, TodoWrite, KillShell, BashOutput

**State-modifying tools** (require guardrails): Edit, Write, Bash, NotebookEdit

**Guardrail detection:** For each state-modifying tool present, the system prompt should contain:
- A "What NOT to Do" section mentioning the tool's risk area, OR
- Explicit restrictions on when/how the tool should be used, OR
- A decision framework for when to modify vs. when to report only

## 5. Model & Permission Checks

| Check | Pass Condition |
|-------|----------------|
| Model valid | `model` is `sonnet`, `opus`, or `haiku` (or absent for inherit) |
| Model appropriate | Model matches task: haiku=simple, sonnet=standard, opus=complex/state-modifying |
| Permission valid | `permissionMode` is `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, or `plan` (or absent) |
| bypassPermissions flagged | If `bypassPermissions`, flag for explicit human review |

**Model appropriateness heuristic:**
- Agent with Edit/Write/Bash tools -> `opus` or `sonnet` recommended (not `haiku`)
- Agent with only Read/Grep/Glob/LS -> `sonnet` or `haiku` appropriate
- Agent with complex reasoning requirements -> `opus` recommended
- Agent with simple pattern matching -> `haiku` appropriate

## 6. System Prompt Checks

| Check | Pass Condition |
|-------|----------------|
| Has role statement | First 5 lines contain "You are" or "You are a" |
| Role not first person | First paragraph does not use "I am" or "I help" |
| Has responsibilities | Contains section with 3-5 bulleted items describing core jobs |
| Has process/strategy | Contains numbered steps or workflow section |
| Has output format | Contains example output template or format specification |
| Has enforcement | Contains "What NOT to Do", "DO NOT", or equivalent negative boundary section |
| Has meta-reminder | Final section reinforces identity or boundaries |
| Line count | Total file under 300 lines |
| No placeholders | No `TODO`, `FIXME`, `XXX`, or `[placeholder]` text |
| No first person framing | System prompt uses "You are...", not "I am..." for identity |

**Enforcement detection:** Look for any of:
- Section heading containing "NOT to Do"
- Section heading containing "NOT"
- Bulleted list of "DO NOT" or "NEVER" items
- "Important:" or "CRITICAL:" sections with restrictions

**Meta-reminder detection:** Look for:
- Final section starting with "REMEMBER:" or "Remember:"
- Closing paragraph that restates the agent's role or boundaries
- Final bold statement summarizing the agent's discipline

## Severity Levels

| Severity | Meaning | Examples |
|----------|---------|----------|
| ERROR | Agent may fail to load or behave incorrectly | Invalid YAML, missing required fields, both tools and disallowedTools |
| WARN | Agent loads but doesn't follow conventions | Missing enforcement section, gerund name, no explicit tool set |
| INFO | Minor improvement suggested | Model could be more appropriate, description could be more specific |

Audit reports should clearly distinguish severity levels.
