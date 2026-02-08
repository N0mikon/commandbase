---
date: 2026-02-07
status: draft
topic: "Phase 3 researching-repo Skill Implementation"
tags: [plan, researching-repo, phase-3, brdspi, research-stack]
git_commit: 3c993c9
references:
  - .docs/research/02-07-2026-phase-3-researching-repo-skill-pre-planning-research.md
  - .docs/plans/02-07-2026-future-skills-implementation-roadmap.md
  - newskills/researching-code/SKILL.md
  - newskills/researching-web/SKILL.md
  - newskills/researching-frameworks/SKILL.md
  - newagents/docs-writer.md
---

# Phase 3: /researching-repo Skill Implementation Plan

## Overview

Build the `/researching-repo` skill — the fourth and final member of the research stack. It clones external git repositories to a system temp directory, analyzes their structure/patterns/conventions using parallel sub-agents, produces a `.docs/research/` artifact via docs-writer, and offers to keep or delete the clone. This completes the research stack: `/researching-web` (community knowledge), `/researching-frameworks` (API docs), `/researching-code` (our code), `/researching-repo` (their code).

## Current State Analysis

Three research skills exist and follow an identical structural template:
- `newskills/researching-code/SKILL.md` (232 lines) — spawns codebase agents on current project
- `newskills/researching-web/SKILL.md` (268 lines) — spawns web-researcher agents
- `newskills/researching-frameworks/SKILL.md` (295 lines) — uses Context7 MCP + web fallback

All three share the same skeleton: Frontmatter → Iron Law → Gate Function → Initial Response → Process Steps → Important Guidelines → Red Flags → Rationalization Prevention → Bottom Line. Each has exactly 2 reference files and 1-2 templates.

No `/researching-repo` skill exists yet. All design decisions are settled in the roadmap (`.docs/plans/02-07-2026-future-skills-implementation-roadmap.md:254-278`) and concept doc (`.docs/future-skills/researching-repo.md`).

### Key Discoveries:
- All research skills use identical section structure — `/researching-repo` must follow the same template exactly
- docs-writer agent (`newagents/docs-writer.md`) expects: `doc_type`, `topic`, `tags`, `content`, optional `references` and `status`
- For research output, docs-writer uses `doc_type: "research"`, routes to `.docs/research/`, default status `complete`
- Security: CVE-2024-32002 requires `core.symlinks=false`, `core.hooksPath=/dev/null`, `--no-recurse-submodules` during clone
- MINGW temp dirs: `mktemp -d -t researching-repo.XXXXXX` works on Git Bash
- Blobless clone (`--filter=blob:none --no-checkout`) preferred; fallback to `--depth=1` for local paths
- Agent path context: Task agents must receive the clone directory path in their prompt to analyze the cloned repo, not the current project

## Desired End State

A fully functional `/researching-repo` skill deployed to `~/.claude/skills/researching-repo/` with:
- `SKILL.md` (~250-300 lines) following the research skill template
- `reference/clone-management.md` (~80-100 lines) covering clone commands, security, cleanup
- `reference/analysis-strategies.md` (~80-100 lines) covering agent decomposition, CLAUDE.md detection
- `templates/repo-research-template.md` (~90-110 lines) with repo-specific output sections

**Verification:** The skill appears in Claude Code's skill list, can be invoked with `/researching-repo <url>`, and produces a `.docs/research/` artifact.

## What We're NOT Doing

- Multi-repo comparison mode (invoke the skill twice and synthesize manually)
- A separate `.docs/patterns/` artifact format (use standard `.docs/research/` for now)
- Sparse checkout for scoped analysis (use `git ls-tree` + `git show` instead)
- Interactive authentication prompts (report failure, let user fix credentials)
- Any changes to existing skills or agents

## Implementation Approach

Create all 4 files in `newskills/researching-repo/`, following the verified patterns from the three existing research skills. Each phase creates one file and is independently verifiable. After all files are created, deploy to global config.

## Phase 1: SKILL.md Core Structure

### Overview
Create the main skill file following the exact research skill template structure. This is the largest and most important file.

### Changes Required:

#### 1. Create `newskills/researching-repo/SKILL.md`
**File**: `newskills/researching-repo/SKILL.md`
**Target**: ~250-300 lines

**Frontmatter** (follow exact pattern from other research skills):
```yaml
---
name: researching-repo
description: "Use this skill when analyzing external git repositories to understand their structure, patterns, and conventions. This includes cloning third-party repos, analyzing directory layouts, architecture patterns, naming conventions, key implementations, and detecting CLAUDE.md/AGENTS.md files. Activate when the user says 'analyze this repo', 'research this repository', 'how does their code work', 'clone and analyze', or provides a git URL for analysis."
---
```

**Section structure** (must follow this exact order):

1. **`# Researching Repositories`** — Opening paragraph describing the task + "Violating the letter..." rule
2. **`## Your Role`** — Analyze external repos: describe structure, patterns, conventions. Do NOT suggest improvements unless asked. Do NOT modify the current project based on findings.
3. **`## The Iron Law`** — `NO SYNTHESIS WITHOUT CLONING AND ANALYZING FIRST` + 4 bullet exceptions:
   - Don't analyze from memory — clone the repo and spawn agents
   - Don't skip the clone for "well-known" repos — every repo gets cloned
   - Don't synthesize partial results — wait for ALL agents to complete
   - Don't skip security mitigations — untrusted repos get full hardening
4. **`## The Gate Function`** — 9 numbered VERB: action steps:
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
5. **`## Initial Response`** — Two conditions:
   - If a git URL or repo identifier was provided → begin cloning immediately
   - If no parameters → prompt with examples:
     ```
     I'll analyze an external repository for you. Please provide a git URL or repository identifier.

     Examples:
     - "https://github.com/user/repo"
     - "git@github.com:user/repo.git"
     - "/c/code/local-repo"
     - "user/repo" (GitHub shorthand)
     ```
6. **`## Analysis Process`** — 7 steps:
   - **Step 1: Clone Repository** — Secure clone using patterns from `./reference/clone-management.md`. Handle GitHub shorthand (expand `user/repo` to `https://github.com/user/repo.git`). Create temp dir, run hardened clone command, verify no hooks.
   - **Step 2: Initial Structure Survey** — Run `git ls-tree -r --name-only HEAD` (or with `-d` for dirs only) to get the full file tree without checking out. Identify key directories, language/framework from file extensions, presence of CLAUDE.md/AGENTS.md.
   - **Step 3: Selective Checkout** — Based on survey, selectively checkout key files needed for analysis: `git show HEAD:path/to/file > /tmp/file`. Focus on: README, CLAUDE.md, AGENTS.md, config files (package.json, Cargo.toml, pyproject.toml, etc.), and files in user-specified scope directories.
   - **Step 4: Spawn Parallel Analysis Agents** — Spawn agents to analyze different aspects. See `./reference/analysis-strategies.md` for decomposition patterns. Each agent prompt MUST include the clone directory path. Minimum 2 agents, typically 3-4.
   - **Step 5: Synthesize Findings** — After ALL agents complete: compile results, connect findings across components, include specific file paths from the cloned repo, document patterns and conventions.
   - **Step 6: Write Research Document** — Spawn `docs-writer` agent via Task tool:
     ```
     Task prompt:
       doc_type: "research"
       topic: "<repo-name> Repository Analysis"
       tags: [repo-analysis, <detected-language>, <detected-framework>]
       references: [<key files discovered during analysis>]
       content: |
         <compiled findings using body sections from ./templates/repo-research-template.md>
     ```
   - **Step 7: Cleanup** — Use AskUserQuestion to offer clone disposition:
     - "Delete clone (default)" — remove temp directory
     - "Keep at current location" — preserve temp dir, show path
     - "Move to a specific path" — let user provide destination
7. **`## Important Guidelines`** — 4 numbered guidelines:
   1. **Analyze, Don't Evaluate** — Describe what IS, not what SHOULD BE. No recommendations unless asked.
   2. **Be Thorough** — Use parallel agents to maximize coverage. Always include file paths from the clone.
   3. **Be Secure** — Always use hardened clone flags. Never skip security mitigations. Verify no hooks after clone.
   4. **Respect the Clone Lifecycle** — Create temp dir, clone securely, analyze, persist findings, then cleanup. Findings must survive clone deletion.
8. **`## Red Flags - STOP and Verify`** — 7 items:
   - Analyzing a repo without cloning it first
   - Cloning without security mitigations (core.symlinks=false, hooksPath=/dev/null)
   - Spawning agents without specifying the clone directory path
   - Synthesizing without spawning parallel agents first
   - Presenting findings without creating a research file first
   - Skipping the keep/delete prompt after analysis
   - Analyzing the current project instead of the clone
9. **`## Rationalization Prevention`** — 7-row table:
   | Excuse | Reality |
   |--------|---------|
   | "I already know this repo" | Your knowledge is stale. Clone and analyze. |
   | "It's a well-known project" | Well-known doesn't mean well-understood. Clone it. |
   | "Cloning takes too long" | Wrong analysis takes longer to fix. Clone. |
   | "Security flags aren't needed for GitHub repos" | Any repo can contain malicious hooks. Always harden. |
   | "I'll skip the research file" | Every analysis produces a file. No exceptions. |
   | "One agent is enough" | One angle isn't analysis. Decompose and parallelize. |
   | "The user just wants a quick look" | Quick looks without evidence are unreliable. Analyze properly. |
10. **`## The Bottom Line`** — Bold + imperative list + bold closing:
    ```
    **No analysis without cloning first.**

    Clone securely. Verify no hooks. Spawn parallel agents. Wait for results. Write the research file. Offer cleanup. THEN present findings.

    This is non-negotiable. Every repo. Every time.
    ```

### Success Criteria:
- [x] File exists at `newskills/researching-repo/SKILL.md`
- [x] Contains all 10 required sections in the correct order
- [x] Frontmatter has `name` and `description` fields only
- [x] Iron Law, Gate Function, Red Flags, Rationalization Prevention, and Bottom Line all present
- [x] docs-writer Task prompt follows the exact format from other research skills
- [x] Security mitigations (CVE-2024-32002) documented in Gate Function and Red Flags
- [x] AskUserQuestion pattern used for cleanup step

---

## Phase 2: Reference Files

### Overview
Create the two reference files that the SKILL.md cross-references. These contain operational details that would bloat the main skill file.

### Changes Required:

#### 1. Create `newskills/researching-repo/reference/clone-management.md`
**File**: `newskills/researching-repo/reference/clone-management.md`
**Target**: ~80-100 lines

**Sections:**

1. **`# Clone Management`** — Brief intro
2. **`## Secure Clone Command`** — The hardened clone command with explanation of each flag:
   ```bash
   git -c core.symlinks=false \
       -c core.hooksPath=/dev/null \
       clone \
       --filter=blob:none \
       --no-checkout \
       --no-recurse-submodules \
       "$url" "$dest"
   ```
   - `core.symlinks=false` — prevents CVE-2024-32002 symlink attack
   - `core.hooksPath=/dev/null` — prevents hook execution
   - `--filter=blob:none` — blobless clone (fast, fetches blobs on demand)
   - `--no-checkout` — delays file materialization
   - `--no-recurse-submodules` — prevents submodule-based attacks
3. **`## Local Path Fallback`** — Local paths and some self-hosted servers don't support partial clone. Detect and fall back:
   ```bash
   # If URL is a local path or file:// protocol, use shallow clone instead
   git -c core.symlinks=false \
       -c core.hooksPath=/dev/null \
       clone \
       --depth=1 \
       --no-recurse-submodules \
       "$url" "$dest"
   ```
   Detection: URL starts with `/`, `./`, `../`, a drive letter (`C:\`), or `file://`
4. **`## Temp Directory Creation`** — MINGW-portable pattern:
   ```bash
   CLONE_DIR=$(mktemp -d -t researching-repo.XXXXXX) || exit 1
   ```
   Falls back through `$TMPDIR` → `$TEMP` → `$TMP` → `/tmp`
5. **`## GitHub Shorthand Expansion`** — Expand `user/repo` to `https://github.com/user/repo.git`. Only apply when input matches `^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$` (no protocol, no slashes beyond the one separator).
6. **`## Post-Clone Security Verification`** — After cloning, check `.git/hooks/` for unexpected files. If any hooks found, remove them before analysis.
7. **`## Cleanup Pattern`** — The keep/delete flow using AskUserQuestion with three options. Include the `chmod -R +w` note for git's read-only `.git` files on Windows.
8. **`## Error Handling`** — Common failure cases and how to handle them:
   - Authentication failure → report clearly, suggest checking SSH keys or HTTPS credentials
   - Network failure → report the error
   - Invalid URL → report and ask user to verify
   - Repository not found → report 404/not-found

#### 2. Create `newskills/researching-repo/reference/analysis-strategies.md`
**File**: `newskills/researching-repo/reference/analysis-strategies.md`
**Target**: ~80-100 lines

**Sections:**

1. **`# Analysis Strategies`** — Brief intro
2. **`## Agent Decomposition`** — How to break repo analysis into parallel agents. Table of recommended agents:
   | Agent | Purpose | Example Prompt |
   |-------|---------|----------------|
   | code-locator | Map directory structure and key files | "List all directories and key files in {clone_dir}. Focus on src/, lib/, and config files." |
   | code-analyzer | Deep analysis of specific components | "Analyze the architecture patterns in {clone_dir}/src/. Document module organization and dependency flow." |
   | code-librarian | Find implementation patterns | "Find examples of how tests are structured in {clone_dir}. Look for test patterns, fixtures, and conventions." |

   Every agent prompt MUST include `{clone_dir}` — agents analyze the clone, not the current project.
3. **`## Full Analysis Decomposition`** — Default 3-4 agent split for full repo analysis:
   - Agent 1: Structure & layout (code-locator) — directory tree, module organization, entry points
   - Agent 2: Architecture & patterns (code-analyzer) — design patterns, dependency flow, abstractions
   - Agent 3: Conventions & config (code-analyzer) — naming conventions, config files, build/test setup
   - Agent 4 (optional): Specific area (code-analyzer) — user-requested deep dive into a subdirectory
4. **`## Scoped Analysis`** — When user targets a specific subdirectory ("just look at `src/skills/`"):
   - Reduce to 2 agents focused on the target area
   - Agent 1: Structure within scope (code-locator)
   - Agent 2: Implementation details within scope (code-analyzer)
5. **`## CLAUDE.md / AGENTS.md Detection`** — Context-aware detection heuristics:
   - Check for presence via `git ls-tree -r HEAD --name-only | grep -i "claude\|agents"`
   - If found, checkout and read the files
   - Classification signals table:
     | Signal | Skills Repo | App Repo |
     |--------|------------|----------|
     | Multiple `*/SKILL.md` files | Yes | No |
     | `skills/` or `commands/` directory | Yes | Unlikely |
     | `src/`, `lib/`, `app/` directories | Unlikely | Yes |
     | `package.json` with `main`/`bin` | No | Yes |
   - Summarization approach:
     - Skills repo: "This is a Claude Code skills repository. CLAUDE.md describes the skill development workflow."
     - App repo: "This project's CLAUDE.md provides development instructions for Claude Code."
     - Unclear: Present both interpretations
6. **`## Accessing File Contents`** — How to read files from a blobless clone without full checkout:
   ```bash
   git show HEAD:path/to/file
   ```
   This fetches the specific blob on demand. Works for individual files without full checkout.

### Success Criteria:
- [x] `newskills/researching-repo/reference/clone-management.md` exists with all 8 sections
- [x] `newskills/researching-repo/reference/analysis-strategies.md` exists with all 6 sections
- [x] Clone command includes all CVE-2024-32002 mitigations
- [x] Local path fallback documented
- [x] Agent prompts show `{clone_dir}` path pattern
- [x] CLAUDE.md/AGENTS.md detection heuristics documented

---

## Phase 3: Output Template

### Overview
Create the repo-specific research document template that defines the body sections for the docs-writer output.

### Changes Required:

#### 1. Create `newskills/researching-repo/templates/repo-research-template.md`
**File**: `newskills/researching-repo/templates/repo-research-template.md`
**Target**: ~90-110 lines

**Sections:**

1. **`# Repository Research Template`** — Brief intro
2. **`## File Naming`** — Format: `MM-DD-YYYY-<repo-name>-repository-analysis.md`. Examples.
3. **`## Body Sections Template`** — The full markdown template:
   ```markdown
   # [Repository Name] Repository Analysis

   **Date**: [Current date]
   **Branch**: [Branch analyzed, typically main/master]
   **Source**: [Git URL]

   ## Research Question
   [What the user wanted to learn about this repository]

   ## Summary
   [2-4 sentences describing what this repo is, what it does, and the key architectural takeaway]

   ## Repository Overview
   - **Purpose**: [What the project does]
   - **Language(s)**: [Primary and secondary languages]
   - **Framework(s)**: [Key frameworks/libraries]
   - **License**: [License type if detected]

   ## Repository Structure
   ```
   [Annotated directory tree showing key directories and their purposes]
   ```

   ## Key Components
   ### [Component/Module 1]
   - **Location**: [directory path]
   - **Purpose**: [What it does]
   - **Key files**: [Important files within]

   ## Architecture Patterns
   [Design patterns, conventions, and architectural decisions observed]
   - [Pattern 1]: [Description with file references]
   - [Pattern 2]: [Description with file references]

   ## Build & Development
   - **Build system**: [How the project is built]
   - **Test framework**: [How tests are run]
   - **Dev workflow**: [How to develop locally]

   ## CLAUDE.md / AGENTS.md Summary
   [If present: context-aware summary. If absent: "Not found in this repository."]

   ## Patterns Worth Adopting
   [Optional section, include only if user requested pattern analysis]

   ## Open Questions
   [Areas that need further investigation or weren't fully covered]
   ```
4. **`## Section Guidelines`** — Guidelines for each section:
   - **Summary**: 2-4 sentences. Answer "what is this and why should I care?" Include the repo URL.
   - **Repository Overview**: Quick-reference metadata. Detect from config files (package.json, Cargo.toml, etc.).
   - **Repository Structure**: Annotated tree. Use `git ls-tree` output. Annotate key directories only, don't list every file.
   - **Key Components**: One subsection per major module. Include file paths from the clone.
   - **Architecture Patterns**: Document what you observe, don't evaluate. Include file references.
   - **Build & Development**: Extract from README, Makefile, package.json scripts, CI configs.
   - **CLAUDE.md / AGENTS.md Summary**: Context-aware (skills repo vs app repo). See analysis-strategies.md.
   - **Patterns Worth Adopting**: Only include if user asked for pattern analysis. List concrete, actionable patterns.
   - **Open Questions**: Areas not fully covered. Suggestions for follow-up.

### Success Criteria:
- [x] `newskills/researching-repo/templates/repo-research-template.md` exists
- [x] Body sections template includes all 9 sections (Research Question through Open Questions)
- [x] Section guidelines provided for each body section
- [x] CLAUDE.md/AGENTS.md section includes context-aware guidance
- [x] File naming convention documented with examples

---

## Phase 4: Deploy and Validate

### Overview
Copy the skill to the global config directory and verify it works.

### Changes Required:

#### 1. Deploy to global config
```bash
cp -r newskills/researching-repo ~/.claude/skills/researching-repo
```

#### 2. Verify skill appears
Check that `/researching-repo` appears in Claude Code's available skills list.

#### 3. Validate structure
Verify the deployed skill has the correct file structure:
```
~/.claude/skills/researching-repo/
├── SKILL.md
├── reference/
│   ├── clone-management.md
│   └── analysis-strategies.md
└── templates/
    └── repo-research-template.md
```

#### 4. Test on a real repository
Run `/researching-repo https://github.com/anthropics/claude-code` (or another suitable public repo) and verify:
- Clone succeeds to temp directory
- Security mitigations applied (no hooks, no symlinks)
- Analysis agents spawn and complete
- `.docs/research/` artifact produced
- Keep/delete prompt appears
- Clone cleanup works

### Success Criteria:
- [x] `/researching-repo` deployed and appears in skill list
- [x] Supports GitHub HTTPS URLs
- [x] Supports GitHub shorthand (`user/repo`)
- [x] Offers to keep clone before cleanup
- [x] Produces useful `.docs/research/` artifact via docs-writer
- [x] Context-aware CLAUDE.md/AGENTS.md detection (when present in target repo)

---

## Testing Strategy

### Per-Phase Verification:
- Phase 1: File exists, all sections present, follows template structure
- Phase 2: Reference files exist, cross-references from SKILL.md resolve
- Phase 3: Template exists, body sections match what SKILL.md describes in Step 6
- Phase 4: End-to-end test on a real public repo

### Regression Check:
- Existing research skills (`researching-code`, `researching-web`, `researching-frameworks`) unmodified
- No changes to `docs-writer` agent or any other agent

## Open Questions Resolved

1. **Blobless vs shallow for local paths?** → Detect local paths and fall back to `--depth=1`
2. **Sparse checkout for scoped analysis?** → No. Use `git ls-tree` + `git show` without checkout
3. **Multiple repos in one session?** → Out of scope. Invoke the skill twice.
4. **Reusable patterns artifact format?** → Use standard `.docs/research/` for now
5. **Agent working directory?** → Pass clone path explicitly in agent prompt text
6. **Authentication failure UX?** → Report failure clearly, don't attempt credential management

## References

- `.docs/research/02-07-2026-phase-3-researching-repo-skill-pre-planning-research.md` — Pre-planning research
- `.docs/plans/02-07-2026-future-skills-implementation-roadmap.md:254-278` — Phase 3 requirements
- `.docs/future-skills/researching-repo.md` — Original concept document
- `newskills/researching-code/SKILL.md` — Pattern source (codebase research)
- `newskills/researching-web/SKILL.md` — Pattern source (web research)
- `newskills/researching-frameworks/SKILL.md` — Pattern source (framework research)
- `newagents/docs-writer.md` — docs-writer agent contract
