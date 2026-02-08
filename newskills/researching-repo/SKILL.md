---
name: researching-repo
description: "Use this skill when analyzing external git repositories to understand their structure, patterns, and conventions. This includes cloning third-party repos, analyzing directory layouts, architecture patterns, naming conventions, key implementations, and detecting CLAUDE.md/AGENTS.md files. Activate when the user says 'analyze this repo', 'research this repository', 'how does their code work', 'clone and analyze', or provides a git URL for analysis."
---

# Researching Repositories

You are tasked with analyzing external git repositories by cloning them securely, spawning parallel analysis agents, and synthesizing findings into a documented research artifact.

**Violating the letter of these rules is violating the spirit of these rules.**

## Your Role

Analyze external repositories to understand their structure, patterns, and conventions:
- Describe what exists: directory layout, architecture, naming conventions, key implementations
- Document how the repository is organized and how components interact
- Detect and summarize CLAUDE.md/AGENTS.md files when present
- Do NOT suggest improvements or changes to the analyzed repo unless explicitly asked
- Do NOT modify the current project based on findings unless explicitly asked

## The Iron Law

```
NO SYNTHESIS WITHOUT CLONING AND ANALYZING FIRST
```

If you haven't cloned the repo and spawned analysis agents, you cannot synthesize findings.

**No exceptions:**
- Don't analyze from memory - clone the repo and spawn agents
- Don't skip the clone for "well-known" repos - every repo gets cloned
- Don't synthesize partial results - wait for ALL agents to complete
- Don't skip security mitigations - untrusted repos get full hardening

## The Gate Function

```
BEFORE completing repository analysis:

1. VALIDATE: Is the input a valid git remote URL or local path?
2. CLONE: Secure clone to system temp directory (see ./reference/clone-management.md)
3. SECURE: Verify no hooks present, symlinks disabled
4. IDENTIFY: What aspects of the repo need investigation?
5. SPAWN: Create parallel analysis agents targeting the clone directory (minimum 2)
6. WAIT: All agents must complete before proceeding
7. VERIFY: Did agents return file:line references from the clone?
   - If NO: Spawn follow-up agents with refined queries
   - If YES: Proceed to synthesis
8. WRITE: Create .docs/research/MM-DD-YYYY-description.md (MANDATORY)
9. CLEANUP: Offer to keep or delete the clone

Skipping clone = analyzing from imagination
Skipping security = risking RCE from untrusted repos
Research without a file = research that will be lost
```

## Initial Response

When this skill is invoked:

1. **If a git URL or repo identifier was provided**, begin cloning immediately
2. **If no parameters provided**, respond with:
```
I'll analyze an external repository for you. Please provide a git URL or repository identifier.

Examples:
- "https://github.com/user/repo"
- "git@github.com:user/repo.git"
- "/c/code/local-repo"
- "user/repo" (GitHub shorthand)
```

Then wait for the user's input.

## Analysis Process

### Step 1: Clone Repository

Secure clone using patterns from `./reference/clone-management.md`:

1. **Expand shorthand**: If input matches `^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$` (no protocol, one separator slash), expand to `https://github.com/<input>.git`
2. **Create temp directory**: `CLONE_DIR=$(mktemp -d -t researching-repo.XXXXXX)`
3. **Determine clone strategy**:
   - Local paths (`/`, `./`, `../`, drive letter, `file://`) → shallow clone with `--depth=1`
   - Remote URLs → blobless clone with `--filter=blob:none --no-checkout`
4. **Execute hardened clone** (always include security flags):
   ```bash
   git -c core.symlinks=false \
       -c core.hooksPath=/dev/null \
       clone \
       --filter=blob:none \
       --no-checkout \
       --no-recurse-submodules \
       "$url" "$CLONE_DIR"
   ```
5. **Post-clone security check**: Verify `.git/hooks/` contains no unexpected files. Remove any found.

If clone fails, report the error clearly and stop. Do not attempt credential management.

### Step 2: Initial Structure Survey

Run `git ls-tree -r --name-only HEAD` in the clone directory to get the full file tree without checking out blobs.

Identify:
- Key directories (src/, lib/, app/, tests/, etc.)
- Language and framework from file extensions and config files
- Presence of CLAUDE.md, AGENTS.md, or similar AI context files
- Entry points (main files, index files, package manifests)

### Step 3: Selective Checkout

Based on the survey, selectively read key files using `git show HEAD:path/to/file`:

- README.md / README
- CLAUDE.md / AGENTS.md (if present)
- Config files: package.json, Cargo.toml, pyproject.toml, go.mod, etc.
- Files in user-specified scope directories

This fetches specific blobs on demand without full checkout.

### Step 4: Spawn Parallel Analysis Agents

Spawn agents to analyze different aspects of the cloned repo. See `./reference/analysis-strategies.md` for decomposition patterns.

**Every agent prompt MUST include the clone directory path.** Agents analyze the clone, not the current project.

**Default decomposition (3-4 agents):**
- Agent 1 (code-locator): Structure and layout — directory tree, module organization, entry points
- Agent 2 (code-analyzer): Architecture and patterns — design patterns, dependency flow, abstractions
- Agent 3 (code-analyzer): Conventions and config — naming conventions, config files, build/test setup
- Agent 4 (code-analyzer, optional): Deep dive into user-specified subdirectory

**Scoped analysis (2 agents):** When user targets a specific subdirectory, reduce to 2 focused agents.

### Step 5: Synthesize Findings

After ALL agents complete:
- Compile results from all agents
- Connect findings across different components
- Include specific file paths from the cloned repo
- Document patterns and conventions observed
- Summarize CLAUDE.md/AGENTS.md content with context-aware interpretation

### Step 6: Write Research Document

Spawn a `docs-writer` agent via the Task tool to create the research file:

```
Task prompt:
  doc_type: "research"
  topic: "<repo-name> Repository Analysis"
  tags: [repo-analysis, <detected-language>, <detected-framework>]
  references: [<key files discovered during analysis>]
  content: |
    <compiled findings using body sections from ./templates/repo-research-template.md>
```

The agent handles frontmatter, file naming, and directory creation.

### Step 7: Cleanup

Use AskUserQuestion to offer clone disposition:

Options:
- **"Delete clone (default)"** — Remove the temp directory
- **"Keep at current location"** — Preserve temp dir, show path
- **"Move to a specific path"** — Let user provide destination

Note: On Windows/MINGW, use `chmod -R +w` before `rm -rf` to handle git's read-only `.git` files.

## Important Guidelines

1. **Analyze, Don't Evaluate**
   - Describe what IS, not what SHOULD BE
   - No recommendations unless asked
   - No critiques or "improvements"

2. **Be Thorough**
   - Use parallel agents to maximize coverage
   - Always include file paths from the clone
   - Connect related components

3. **Be Secure**
   - Always use hardened clone flags
   - Never skip security mitigations
   - Verify no hooks after clone

4. **Respect the Clone Lifecycle**
   - Create temp dir, clone securely, analyze, persist findings, then cleanup
   - Findings must survive clone deletion
   - Always offer the keep/delete choice

## Red Flags - STOP and Verify

If you notice any of these, pause:

- Analyzing a repo without cloning it first
- Cloning without security mitigations (core.symlinks=false, hooksPath=/dev/null)
- Spawning agents without specifying the clone directory path
- Synthesizing without spawning parallel agents first
- Presenting findings without creating a research file first
- Skipping the keep/delete prompt after analysis
- Analyzing the current project instead of the clone

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I already know this repo" | Your knowledge is stale. Clone and analyze. |
| "It's a well-known project" | Well-known doesn't mean well-understood. Clone it. |
| "Cloning takes too long" | Wrong analysis takes longer to fix. Clone. |
| "Security flags aren't needed for GitHub repos" | Any repo can contain malicious hooks. Always harden. |
| "I'll skip the research file" | Every analysis produces a file. No exceptions. |
| "One agent is enough" | One angle isn't analysis. Decompose and parallelize. |
| "The user just wants a quick look" | Quick looks without evidence are unreliable. Analyze properly. |

## The Bottom Line

**No analysis without cloning first.**

Clone securely. Verify no hooks. Spawn parallel agents. Wait for results. Write the research file. Offer cleanup. THEN present findings.

This is non-negotiable. Every repo. Every time.
