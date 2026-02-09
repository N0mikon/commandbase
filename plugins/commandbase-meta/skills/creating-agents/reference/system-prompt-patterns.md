# System Prompt Patterns

The system prompt is the body of an agent's `.md` file - everything after the YAML frontmatter. It defines the agent's behavior, boundaries, and output quality.

## The Contract Format

Structure every system prompt using these sections in order:

### 1. Role Statement (1-2 lines)

State what the agent is and its core purpose. Use "You are..." framing.

```markdown
You are a specialist at locating files, directories, and components in codebases.
Your job is to find WHERE things are, not to analyze WHAT they do.
```

### 2. Core Responsibilities (3-5 bullets)

Define the agent's jobs explicitly. These are the things it MUST do.

```markdown
## Core Responsibilities

1. **Find by topic**: Given a feature or concept, locate all relevant files
2. **Categorize results**: Group findings by type (implementation, test, config, types)
3. **Return organized results**: Present findings in a scannable format with file paths
```

### 3. Strategy/Process (numbered steps)

How the agent should approach its work. This is the workflow.

```markdown
## Search Strategy

1. Start with broad glob patterns to identify candidate files
2. Refine with grep to find specific code patterns
3. Categorize results by file type and purpose
4. Present organized results with file paths
```

### 4. Output Format (with example)

Show exactly what good output looks like. Include a concrete template.

```markdown
## Output Format

Present findings in this structure:

### [Topic/Feature Name]

**Implementation:**
- `src/auth/login.ts` - Main login flow
- `src/auth/session.ts` - Session management

**Tests:**
- `tests/auth/login.test.ts` - Login unit tests

**Configuration:**
- `config/auth.json` - Auth provider settings
```

### 5. Guidelines (positive rules)

What the agent should do and how. These are the guardrails.

```markdown
## Important Guidelines

- Always include file paths relative to the project root
- When uncertain about a match, include it with a note rather than omitting
- If no results found, say so explicitly rather than returning empty results
- Prefer showing 3 specific matches over 20 vague ones
```

### 6. What NOT to Do (negative enforcement)

Explicit boundaries. What the agent must never do. This section is critical for constrained agents.

```markdown
## What NOT to Do

- Do NOT read file contents unless explicitly needed (you're a locator, not an analyzer)
- Do NOT suggest improvements or refactoring to found code
- Do NOT provide opinions on code quality
- Do NOT modify any files
- Do NOT execute commands beyond search tools
```

### 7. Meta-Reminder (1-2 lines, closing)

Reinforce the agent's identity at the end. This combats drift during long interactions.

```markdown
Remember: you are a file finder and organizer, not a code analyst. Your job is to
locate and categorize, not to evaluate or suggest.
```

## Enforcement Patterns

Different agent types need different levels of enforcement:

### Read-Only Agents (locators, analyzers, researchers)

Heavy emphasis on what NOT to do, because the risk is scope creep into modification:

```markdown
## CRITICAL

Do NOT:
- Suggest code changes or improvements
- Provide opinions on architecture
- Make modifications to any files
- Run commands that change state

You are a documentarian, not a consultant.
```

### State-Modifying Agents (updaters, builders)

Emphasis on decision trees and conservative defaults:

```markdown
## Decision Framework

**Archive if:**
- Document hasn't been referenced in 30+ days
- Core topic no longer exists in codebase

**Update if:**
- Document is still relevant but contains stale information
- Referenced files have changed significantly

**When uncertain: prefer update over archive.**
```

### Research Agents (web researchers, code researchers)

Emphasis on source quality and uncertainty handling:

```markdown
## Source Authority

Prefer sources in this order:
1. Official documentation
2. Recognized experts
3. Community consensus
4. Blog posts and tutorials

## Uncertainty Handling

- If conflicting information is found, present all sides with sources
- If information cannot be verified, say so explicitly
- Never present uncertain findings as definitive
```

## Model-Specific Guidance

| Model | Best For | Prompt Style |
|-------|----------|-------------|
| `haiku` | Fast, simple tasks (locating, categorizing) | Tight constraints, simple output format |
| `sonnet` | Standard tasks (analysis, research, review) | Full Contract Format, moderate enforcement |
| `opus` | Complex reasoning, state modification | Detailed decision trees, extensive guardrails |

## Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| No role statement | Agent doesn't know its identity | Add "You are..." opener |
| Vague responsibilities | Agent does too much or too little | Define 3-5 specific jobs |
| No output format | Inconsistent, unusable output | Add example template |
| No negative enforcement | Agent drifts into unintended behaviors | Add "What NOT to Do" section |
| Too prescriptive for a creative task | Agent produces rigid, unhelpful output | Raise freedom tier, use principles over steps |
| No meta-reminder | Agent forgets its role in long interactions | Add closing identity reinforcement |

## Size Guidelines

| Agent Type | Target Lines | Notes |
|-----------|-------------|-------|
| Simple locator/finder | 60-100 | Tight scope, few tools |
| Standard analyzer/researcher | 100-180 | Full Contract Format |
| Complex state-modifier | 150-250 | Detailed decision trees, extensive guardrails |
| Maximum recommended | 300 | Beyond this, consider splitting into multiple agents |
