# Question Design Principles

Guidelines for crafting interactive discovery questions during project setup.

## Always Include an "Explain This" Option

When asking about technical choices, include:
```json
{
  "label": "Explain these options",
  "description": "I'd like to understand the tradeoffs before deciding"
}
```
When user selects this, provide a concise explanation of each option and its tradeoffs, then re-ask the question.

## Mark Recommended Options Based on Prior Answers

- After learning the project type and tech stack, infer sensible defaults
- Add "(Recommended)" to the label of the suggested option
- Always put the recommended option first in the list

## Suggest Based on Context

| Prior Answer | Suggests |
|--------------|----------|
| Python project | pytest, ruff, pyproject.toml |
| TypeScript/Node | vitest or jest, biome or eslint |
| CLI tool | Minimal deps, clear --help |
| Web app | Docker, CI/CD, env management |
| Solo project | Simpler workflow, less ceremony |

## Discovery Rounds

### Round 1: Core Identity
- **Project type**: What kind of project is this? (web app, CLI tool, API service, library, mobile app, etc.)
- **Primary language/framework**: What's the main technology? (e.g., TypeScript/React, Python/FastAPI, Go, Rust, etc.)
- **Project purpose**: What problem does this solve? (1-2 sentence description)

### Round 2: Technical Details
Based on Round 1 answers, ask about:
- **Package manager**: Which package manager? (npm, pnpm, bun, pip, cargo, etc.)
- **Testing framework**: Preferred testing approach? (jest, vitest, pytest, go test, etc.)
- **Additional tooling**: Any specific tools required? (Docker, database, CI/CD preferences)

### Round 3: Development Workflow
- **Build/run commands**: Any specific commands for building and running?
- **Code quality**: Linter/formatter preferences? (eslint, biome, ruff, etc.)
- **Special requirements**: Any constraints, integrations, or non-standard needs?

### Round 4: Scope & Goals (Optional)
If the project seems complex, ask:
- **MVP scope**: What's the minimum viable first version?
- **Key features**: What are the 3-5 most important features?

**Important**: Adapt questions based on previous answers. Skip irrelevant questions. Don't ask about things you can infer.
