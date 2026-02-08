# Analysis Strategies

Guide to decomposing repository analysis into parallel sub-agents for comprehensive coverage. Each strategy targets different aspects of a repository.

## Agent Decomposition

Break repo analysis into parallel agents using specialized agent types. Each agent focuses on a different analysis dimension.

| Agent | Purpose | Example Prompt |
|-------|---------|----------------|
| **code-locator** | Map directory structure and key files | "List all directories and key files in {clone_dir}. Focus on src/, lib/, and config files. Return file paths with brief descriptions." |
| **code-analyzer** | Deep analysis of specific components | "Analyze the architecture patterns in {clone_dir}/src/. Document module organization, dependency flow, and key abstractions." |
| **code-librarian** | Find implementation patterns | "Find examples of how tests are structured in {clone_dir}. Look for test patterns, fixtures, and conventions." |

**Every agent prompt MUST include `{clone_dir}`.** Agents analyze the cloned repository, not the current project. Without the explicit path, agents will default to searching the working directory.

## Full Analysis Decomposition

Default 3-4 agent split for comprehensive repo analysis:

**Agent 1: Structure & Layout** (code-locator)
- Directory tree and module organization
- Entry points (main files, index files, CLI commands)
- Key configuration files
- Prompt: "Map the complete directory structure of {clone_dir}. Identify entry points, key modules, and the overall organization pattern. Focus on top-level directories and their purposes."

**Agent 2: Architecture & Patterns** (code-analyzer)
- Design patterns used (MVC, plugin system, middleware, etc.)
- Dependency flow between modules
- Key abstractions and interfaces
- Prompt: "Analyze the architecture and design patterns in {clone_dir}. Document how modules depend on each other, what abstractions are used, and the overall architectural style. Include file:line references."

**Agent 3: Conventions & Config** (code-analyzer)
- Naming conventions (files, functions, variables)
- Configuration approach (env vars, config files, constants)
- Build system and test setup
- Prompt: "Analyze conventions and configuration in {clone_dir}. Document naming patterns, config file formats, build commands, test framework setup, and CI/CD configuration. Include file:line references."

**Agent 4: Specific Area** (code-analyzer, optional)
- Only spawn when user requests deep dive into a specific subdirectory
- Prompt: "Analyze {clone_dir}/{user_specified_path}/ in depth. Document the module's internal structure, key functions, data flow, and how it integrates with the rest of the project. Include file:line references."

## Scoped Analysis

When user targets a specific subdirectory ("just look at `src/skills/`"), reduce to 2 focused agents:

**Agent 1: Structure Within Scope** (code-locator)
- File listing and organization within the target directory
- How the scoped area relates to the broader project
- Prompt: "Map the structure of {clone_dir}/{scope}/. List all files, identify sub-modules, and describe how this directory fits into the broader project."

**Agent 2: Implementation Details** (code-analyzer)
- Deep analysis of code within the target directory
- Patterns, conventions, and key implementations
- Prompt: "Analyze the implementation in {clone_dir}/{scope}/. Document key functions, patterns used, data flow, and conventions. Include file:line references for all findings."

## CLAUDE.md / AGENTS.md Detection

Check for AI context files during the initial structure survey:

```bash
git ls-tree -r HEAD --name-only | grep -i "claude\|agents"
```

If found, checkout and read these files using `git show HEAD:path/to/file`.

**Classification signals** to determine repository type:

| Signal | Skills Repo | App Repo |
|--------|------------|----------|
| Multiple `*/SKILL.md` files | Yes | No |
| `skills/` or `commands/` directory | Yes | Unlikely |
| `src/`, `lib/`, `app/` directories | Unlikely | Yes |
| `package.json` with `main`/`bin` | No | Yes |

**Summarization approach based on classification:**
- **Skills repo**: "This is a Claude Code skills repository. CLAUDE.md describes the skill development workflow."
- **App repo**: "This project's CLAUDE.md provides development instructions for Claude Code."
- **Unclear**: Present both interpretations and let the user decide.

Always include the full CLAUDE.md/AGENTS.md content in the research document, not just a summary. These files are high-value context.

## Accessing File Contents

Read files from a blobless clone without full checkout:

```bash
git show HEAD:path/to/file
```

This fetches the specific blob on demand from the remote. Works for individual files without requiring `git checkout`.

**Common patterns:**
```bash
# Read a specific file
git show HEAD:README.md

# Read a config file
git show HEAD:package.json

# Read a nested file
git show HEAD:src/index.ts

# List directory contents (use ls-tree instead)
git ls-tree HEAD src/
```

Use `git show` for file content and `git ls-tree` for directory listings. Both work without checkout.
