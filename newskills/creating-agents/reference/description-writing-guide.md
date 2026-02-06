# Description Writing Guide

The description field is the most critical part of an agent. It determines when the orchestrator delegates work to the agent - every other part of the agent is wasted if the description doesn't trigger delegation correctly.

## The Delegation Trigger Formula

```
"[What it does in one sentence]. [When to delegate to it - the trigger]."
```

The formula works because:
- The first sentence tells the orchestrator what capability the agent provides
- The second sentence tells the orchestrator when to reach for this agent specifically
- Together they enable the orchestrator to match task requirements to agent capabilities

## How Agent Descriptions Differ from Skill Descriptions

| Aspect | Agent Description | Skill Description |
|--------|------------------|-------------------|
| Opener | Capability statement | "Use this skill when..." |
| Audience | The orchestrator (another Claude instance) | Claude matching user intent |
| Trigger | Explicit delegation decision | Implicit intent matching |
| Voice | Third-person declarative | Third-person instructional |
| Mental model | "This specialist handles X" | "The user is doing X" |

Skills need intent-matching keywords because they activate implicitly. Agents need clear capability statements because they're delegated to explicitly.

## Good Examples

### Example 1: Codebase analysis agent

```yaml
description: Analyzes codebase implementation details. Call the codebase-analyzer
  agent when you need to find detailed information about specific components.
```

**Why it works:**
- Capability: "Analyzes codebase implementation details" - clear scope
- Trigger: "when you need to find detailed information about specific components" - clear delegation condition
- Distinguishable: not a locator (finds files) or pattern-finder (finds examples)

### Example 2: Document locator agent

```yaml
description: Finds relevant documents across .docs/ directory (plans, research,
  handoffs). Use when you need to discover what documentation exists about a topic
  before creating new docs or when looking for historical context.
```

**Why it works:**
- Capability: "Finds relevant documents across .docs/ directory" - scoped to specific area
- Trigger: "when you need to discover what documentation exists" - clear condition
- Bonus: "before creating new docs or when looking for historical context" - two concrete scenarios

### Example 3: Web research agent

```yaml
description: Searches the web and fetches page content to find current, sourced
  information. Use when you need up-to-date information beyond training data -
  API docs, best practices, library comparisons, error solutions, or any question
  where recency matters.
```

**Why it works:**
- Capability: "Searches the web and fetches page content" - describes mechanism
- Trigger: "when you need up-to-date information beyond training data" - clear gap this fills
- Specifics: "API docs, best practices, library comparisons, error solutions" - concrete examples

## Bad Examples and Fixes

### Bad Example 1: Too vague

```yaml
description: Helps with code stuff.
```

**Problems:** No capability statement, no delegation trigger, matches nothing specifically.

**Fixed:**
```yaml
description: Reviews code changes for bugs, security issues, and style violations.
  Call when you need a quality check before committing or when reviewing a pull request.
```

### Bad Example 2: Missing trigger

```yaml
description: Can read files and search for patterns in codebases.
```

**Problems:** Describes capability but not when to delegate. The orchestrator can read files itself - why use this agent?

**Fixed:**
```yaml
description: Finds similar implementations, usage examples, and existing patterns
  that can be modeled after. Use when you need concrete code examples to inform
  new development.
```

### Bad Example 3: Skill-style description on an agent

```yaml
description: "Use this skill when analyzing code quality and looking for bugs."
```

**Problems:** Uses skill formula ("Use this skill when...") on an agent. Agents aren't skills.

**Fixed:**
```yaml
description: Analyzes code quality and identifies bugs, logic errors, and security
  vulnerabilities. Call when code needs a thorough review beyond surface-level scanning.
```

### Bad Example 4: Indistinguishable from siblings

```yaml
# Two agents in the same family with overlapping descriptions
description: Analyzes codebases to find information.  # Agent A
description: Finds information in codebases.           # Agent B
```

**Problems:** The orchestrator can't tell when to use A vs B.

**Fixed:**
```yaml
description: Analyzes codebase implementation details. Call when you need
  to understand how specific components work internally.       # Agent A: deep analysis
description: Locates files, directories, and components relevant to a feature
  or task. Call when you need to find where things are.        # Agent B: finding locations
```

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Too vague | Orchestrator can't distinguish from general capability | Add specific scope and concrete trigger |
| Missing trigger | Orchestrator doesn't know when to delegate | Add "Call when..." or "Use when..." clause |
| Skill-style formula | Wrong activation model - agents use delegation, not intent matching | Use capability + trigger formula |
| Overlapping siblings | Orchestrator picks the wrong agent | Differentiate by scope, depth, or output type |
| First person | "I analyze code" doesn't match delegation evaluation | Use third person: "Analyzes code..." |
| Keyword stuffing | Reads like search spam, confuses rather than clarifies | Use natural language with embedded specifics |

## Writing Process

1. **Identify the delegation gap**: What task would the orchestrator struggle to do in its main context? That's what the agent solves.

2. **Write the capability statement**: One sentence describing what the agent does. Be specific about scope and mechanism.

3. **Write the trigger clause**: One sentence describing when to delegate. Include the condition that makes this agent the right choice over doing it inline.

4. **Differentiate from siblings**: If there are related agents, ensure the description clearly separates this agent's scope. Use different verbs, scopes, or output types.

5. **Validate constraints:**
   - Under 1024 characters?
   - No angle brackets (`<` or `>`)?
   - Not first person?
   - Clear delegation trigger present?
   - Distinguishable from similar agents?

6. **Test mentally:** Read the description and ask: "If the orchestrator had [task], would it select this agent?" Try 3 different task phrasings.
