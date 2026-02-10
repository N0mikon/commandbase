---
date: 2026-02-07
status: archived
topic: "Phase 3 /researching-repo Skill - Pre-Planning Research"
tags: [research, researching-repo, phase-3, brdspi, research-stack]
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Archived — all newskills/newagents references dead after plugin restructure (87a19a3). Skill shipped at plugins/commandbase-research/skills/researching-repo/."
archived: 2026-02-09
archive_reason: "Research fully consumed; referenced newskills/* and newagents/* paths deleted in plugin restructure commit 87a19a3. Skill shipped at plugins/commandbase-research/skills/researching-repo/."
references:
  - .docs/plans/02-07-2026-future-skills-implementation-roadmap.md
  - .docs/future-skills/researching-repo.md
  - .docs/research/02-07-2026-phase-2-brdspi-core-research.md
  - newskills/researching-code/SKILL.md
  - newskills/researching-web/SKILL.md
  - newskills/researching-frameworks/SKILL.md
  - newskills/starting-projects/SKILL.md
  - newagents/docs-writer.md
  - newskills/researching-repo/SKILL.md
  - newskills/researching-repo/reference/clone-management.md
  - newskills/researching-repo/reference/analysis-strategies.md
  - newskills/researching-repo/templates/repo-research-template.md
---

# Phase 3 /researching-repo Skill - Pre-Planning Research

**Date**: 2026-02-07
**Branch**: master

## Research Question

What does the current codebase look like, what patterns exist, and what decisions have already been made — so that a Phase 3 implementation plan can be written with full context for building the `/researching-repo` skill?

## Summary

Phase 3 adds the final research skill (`/researching-repo`) to complete the research stack: web, frameworks, code, and repo. The skill clones external repositories to a system temp directory, analyzes their structure/patterns/conventions using parallel sub-agents, produces a `.docs/research/` artifact, and offers to keep or delete the clone. This research documents the existing patterns across all three research skills, git clone mechanics for MINGW/Windows, CLAUDE.md/AGENTS.md detection requirements, security considerations, and docs-writer integration — everything needed to write an implementation plan.

## Implementation Status

This research has been fully consumed. The `/researching-repo` skill was implemented and deployed with the exact structure proposed in Section 11:

```
newskills/researching-repo/
├── SKILL.md                           (223 lines)
├── reference/
│   ├── clone-management.md            (118 lines)
│   └── analysis-strategies.md         (108 lines)
└── templates/
    └── repo-research-template.md      (136 lines)
```

The skill has been deployed to `~/.claude/skills/researching-repo/` and is live. The research stack is now complete: `/researching-web`, `/researching-frameworks`, `/researching-code`, and `/researching-repo`.

## Scope: 1 Work Item

| Item | Type | Complexity | Key Challenge |
|------|------|-----------|---------------|
| 3. `/researching-repo` | New skill | Medium | Clone management, security, cross-platform temp dirs, context-aware file detection |

## Detailed Findings

### 1. Design Decisions Already Made (from roadmap and concept doc)

These decisions are settled and should NOT be re-debated during planning:

**Cloning:**
- Clone any git repo (shallow clone to **system temp dir**)
- Before cleanup, offer: "Keep this clone somewhere? (provide path or skip to delete)"
- Supports any git remote: GitHub, GitLab, Bitbucket, LinuxServer, local paths

**Analysis:**
- Directory layout, architecture patterns, naming conventions, key implementations
- Scoped analysis: user can target specific directories ("just look at `src/skills/`")

**CLAUDE.md/AGENTS.md detection:**
- Detect if present, summarize with context awareness
- In a skills repo: they're the product
- In an app repo: they're dev tooling

**Output:**
- Produce `.docs/research/` artifact via docs-writer agent
- Artifact survives clone deletion
- Could produce a reusable "patterns" artifact that `/designing-code` or `/structuring-code` can reference

**Naming convention:**
- `researching-repo` (gerund + domain, consistent with researching-code, researching-web, researching-frameworks)

**Open questions from concept doc (now resolved by roadmap and this research):**
- Where to clone? **System temp dir** (`mktemp -d` on MINGW/Git Bash)
- Non-GitHub repos? **Yes** — any git remote (GitHub, GitLab, Bitbucket, local paths)
- Large repos? **Blobless clone** (`--filter=blob:none --no-checkout`) for structure analysis without downloading file contents
- CLAUDE.md/AGENTS.md detection? **Yes** with context awareness
- Reusable patterns artifact? **Yes** — decision deferred to planning

### 2. Existing Research Skill Patterns (Cross-Skill Analysis)

All three existing research skills (`researching-code`, `researching-web`, `researching-frameworks`) follow a consistent structural template. `/researching-repo` must follow the same template.

**Structural elements ALL three skills share:**
1. Iron Law (1-line imperative in code fence + 4 bullet exceptions)
2. Gate Function (7-8 numbered VERB: action steps in code fence)
3. Initial Response (conditional on parameters provided vs not)
4. Step-based Process (5-7 numbered steps)
5. Write step using docs-writer via Task tool
6. Reference files (exactly 2 per skill)
7. Templates directory (1-2 templates per skill)
8. Red Flags section
9. Rationalization Prevention table
10. The Bottom Line (bold + imperative list + bold closing)

**Iron Law patterns:**
- `/researching-code`: "NO SYNTHESIS WITHOUT PARALLEL RESEARCH FIRST"
- `/researching-web`: "NO SYNTHESIS WITHOUT PARALLEL WEB RESEARCH FIRST"
- `/researching-frameworks`: "NO RECOMMENDATION WITHOUT CURRENT DOCUMENTATION"
- `/researching-repo` candidate: "NO SYNTHESIS WITHOUT CLONING AND ANALYZING FIRST"

**Gate Function patterns:**
- All use numbered steps with `VERB: action` format
- All include VERIFY step with if/then branching
- All end with consequences of skipping steps
- `/researching-repo` will need unique steps for clone, security check, and cleanup

**Agent spawning patterns:**
- `/researching-code`: spawns `code-locator`, `code-analyzer`, `code-librarian`, `docs-locator`, `docs-analyzer` agents
- `/researching-web`: spawns `web-researcher` agents with different search angles
- `/researching-frameworks`: uses Context7 MCP tools directly + web-researcher fallback
- `/researching-repo`: will likely spawn codebase analysis agents (similar to researching-code) operating on the cloned repo

**File counts and structure (pattern to follow):**
```
newskills/researching-code/
├── SKILL.md                           (232 lines)
├── reference/
│   ├── research-agents.md             (71 lines)
│   └── evidence-requirements.md       (65 lines)
└── templates/
    └── research-document-template.md  (85 lines)

newskills/researching-web/
├── SKILL.md                               (268 lines)
├── reference/
│   ├── search-strategies.md               (124 lines)
│   └── evidence-requirements.md           (92 lines)
└── templates/
    └── web-research-document-template.md  (100 lines)

newskills/researching-frameworks/
├── SKILL.md                                  (295 lines)
├── reference/
│   ├── context7-usage.md                     (117 lines)
│   └── research-tiers.md                     (108 lines)
└── templates/
    ├── framework-research-template.md        (153 lines)
    └── architecture-decision-template.md     (93 lines)
```

### 3. Git Clone Mechanics for MINGW/Windows

**Recommended clone approach: Blobless clone with --no-checkout**

```bash
git clone --filter=blob:none --no-checkout <url> <destination>
```

This downloads all commits and trees but not file contents. Commands like `git log`, `git ls-tree -r HEAD`, and `git log -- <path>` work without additional downloads. File contents can be fetched on-demand with `git show HEAD:path/to/file`.

**Performance comparison:**

| Clone Type | Speed | Best For |
|------------|-------|----------|
| Blobless (`--filter=blob:none`) | Fast initial, efficient access | Structure analysis (recommended) |
| Treeless (`--filter=tree:0`) | Fastest initial | Single-use CI builds (not recommended) |
| Shallow (`--depth=1`) | Fastest initial | Quick disposal (alternative option) |

**Note:** Blobless clone requires server-side support. GitHub, GitLab, Bitbucket, and Azure DevOps all support it. Local paths and self-hosted Git servers may not — fallback to `--depth=1` for those.

**Temp directory (MINGW/Git Bash portable pattern):**

```bash
CLONE_DIR=$(mktemp -d -t researching-repo.XXXXXX) || exit 1
```

- `mktemp` is available in modern Git Bash (included in MSYS2 runtime)
- `-t` flag uses the system temp directory
- `XXXXXX` adds random suffix for uniqueness
- Falls back through `$TMPDIR` → `$TEMP` → `$TMP` → `/tmp`

**Supported git remote formats:**

| Format | Example |
|--------|---------|
| HTTPS | `https://github.com/user/repo.git` |
| SSH (SCP-style) | `git@github.com:user/repo.git` |
| SSH (full) | `ssh://git@github.com/user/repo.git` |
| Git protocol | `git://server.com/path/to/repo.git` |
| File protocol | `file:///C:/code/repo` |
| Local path | `/c/code/repo`, `C:\code\repo`, `../relative/path` |

**Windows path handling:**
```bash
# Convert Windows paths to MINGW paths if needed
if [[ "$repo_path" =~ ^[A-Za-z]:\\ ]]; then
    repo_path=$(cygpath -u "$repo_path")
fi
```

### 4. Security Considerations

**Critical: CVE-2024-32002 — Remote Code Execution via git clone**

Repositories with crafted submodules can inject executable hooks (e.g., `post-checkout`) that run during clone via symlink manipulation. This allows RCE before code inspection.

**Required mitigations for `/researching-repo`:**

```bash
git -c core.symlinks=false \
    -c core.hooksPath=/dev/null \
    clone \
    --filter=blob:none \
    --no-checkout \
    --no-recurse-submodules \
    "$url" "$dest"
```

Key flags:
- `core.symlinks=false` — prevents the CVE-2024-32002 attack vector
- `core.hooksPath=/dev/null` — prevents hook execution
- `--no-checkout` — delays file materialization
- `--no-recurse-submodules` — prevents submodule-based attacks

**Post-clone verification:**
- Check `.git/hooks/` for unexpected files
- Remove any hooks found before analysis

**Authentication handling:**
- SSH keys and credential helpers work normally
- Skill should handle auth failures gracefully with clear error messages
- Private repos require authentication; skill should not attempt to store or prompt for credentials

### 5. Cleanup Pattern

**Recommended: trap EXIT with conditional keep**

```bash
cleanup() {
    if [[ "$KEEP_REPO" == "true" ]]; then
        echo "Repository kept at: $CLONE_DIR"
    elif [[ -d "$CLONE_DIR" ]]; then
        chmod -R +w "$CLONE_DIR" 2>/dev/null || true  # git makes .git files read-only
        rm -rf "$CLONE_DIR"
    fi
}
trap cleanup EXIT INT TERM
```

**"Keep or delete" prompt pattern (from roadmap):**
- After analysis completes, use AskUserQuestion:
  - "Delete clone (default)" — cleanup temp dir
  - "Keep at current location" — preserve temp dir, show path
  - "Move to a specific path" — let user provide a path

### 6. CLAUDE.md/AGENTS.md Context-Aware Detection

**Current state:** No implementation exists for repo type classification. This is net-new functionality for `/researching-repo`.

**Existing patterns to build on:**
- `/updating-claude-md` (SKILL.md:42-63) — path-based scope detection (global vs project CLAUDE.md)
- `/starting-projects` (question-design.md:23-31) — context-based suggestions adapting to prior answers

**Proposed detection heuristics (for planning):**

| Signal | Skills Repo | App Repo |
|--------|------------|----------|
| Multiple `*/SKILL.md` files | Yes | No |
| `skills/` or `commands/` directory | Yes | Unlikely |
| `AGENTS.md` with agent specs | Yes (product) | Maybe (tooling) |
| `src/`, `lib/`, `app/` directories | Unlikely | Yes |
| `package.json` with `main`/`bin` | No | Yes |
| CLAUDE.md mentions "skills" as product | Yes | No |
| CLAUDE.md mentions app architecture | No | Yes |

**Summarization approach:**
- **Skills repo:** "This is a Claude Code skills repository. The CLAUDE.md describes the skill development workflow. Skills in `[dir]/` are the product."
- **App repo:** "This project's CLAUDE.md provides development instructions and project context for Claude Code."
- **Both/unclear:** Present both interpretations, let user decide relevance

### 7. docs-writer Integration Pattern

`/researching-repo` follows the standard docs-writer delegation pattern used by all research skills:

```markdown
Spawn a `docs-writer` agent via the Task tool:

Task prompt:
  doc_type: "research"
  topic: "<repo-name> Repository Analysis"
  tags: [repo-analysis, <detected-language>, <detected-framework>]
  references: [<key files discovered during analysis>]
  content: |
    <compiled findings using repo research template>
```

**Custom template needed:** `templates/repo-research-template.md` with sections specific to external repo analysis:
- Repository Overview (what it is, what it does)
- Repository Structure (directory layout with annotations)
- Technology Stack (languages, frameworks, tools)
- Key Components (major modules and their purposes)
- Architecture Patterns (design patterns, conventions)
- CLAUDE.md/AGENTS.md Summary (context-aware, when present)
- Build & Development (how to build/test/run)
- Patterns Worth Adopting (optional, if user requests)
- Open Questions

### 8. Unique Aspects of /researching-repo (vs Other Research Skills)

| Aspect | researching-code | researching-web | researching-frameworks | researching-repo |
|--------|-----------------|----------------|----------------------|-----------------|
| Source | Current project | Web | MCP + Web | Cloned external repo |
| Pre-work | None | None | Context7 detection | Clone + security check |
| Agents | Codebase agents | web-researcher | Context7 + web-researcher | Codebase agents on clone |
| Cleanup | None | None | None | Delete/keep clone |
| Security | None needed | None needed | None needed | Clone security mitigations |
| Output | `.docs/research/` | `.docs/research/` | `.docs/references/` | `.docs/research/` |
| Modes | 1 | 1 | 3 (standalone, delegated, adding dep) | 2+ (full analysis, scoped analysis) |

**Unique challenges for /researching-repo:**
1. **Clone lifecycle management** — create temp dir, clone securely, analyze, cleanup
2. **Agent path context** — sub-agents need to know they're analyzing the clone dir, not the current project
3. **Security hardening** — untrusted repos need CVE mitigations
4. **Cross-platform temp handling** — MINGW/Git Bash compatibility
5. **Context-aware detection** — net-new feature for classifying repo type
6. **Scoped analysis** — user can target specific subdirectories within the repo
7. **Keep/delete decision** — interactive prompt after analysis

### 9. Reference Files to Create (2 files, following pattern)

Based on the pattern of exactly 2 reference files per research skill:

**Reference 1: `reference/clone-management.md`**
- Clone command patterns (blobless, shallow, local)
- Security flags and mitigations
- Temp directory creation
- Cleanup and keep/delete flow
- Windows/MINGW path handling
- Error handling for auth failures

**Reference 2: `reference/analysis-strategies.md`**
- What to analyze and how
- Agent decomposition patterns (which agents to spawn and what to ask them)
- CLAUDE.md/AGENTS.md detection heuristics
- Scoped vs full analysis
- Repo type classification signals

### 10. Template to Create (1 file)

**`templates/repo-research-template.md`**
- Repository-specific body sections (see Section 7 above)
- Guidelines for each section
- Adapted from `researching-code/templates/research-document-template.md` pattern

### 11. Proposed Skill Structure

```
newskills/researching-repo/
├── SKILL.md                           (~250-300 lines target)
├── reference/
│   ├── clone-management.md            (~80-100 lines)
│   └── analysis-strategies.md         (~80-100 lines)
└── templates/
    └── repo-research-template.md      (~90-110 lines)
```

### 12. Workflow Integration

`/researching-repo` completes the research stack and can be used:

**During BRDSPI Research phase (all four in parallel):**
```
/researching-web      — landscape and community consensus
/researching-frameworks — API docs of dependencies
/researching-repo     — reference implementation patterns
/researching-code     — current project's existing state
```

**Standalone use cases:**
- Pre-contribution analysis of open source projects
- Library evaluation (understand internals, not just API surface)
- Pattern stealing from well-architected projects
- Comparative analysis (clone two repos, analyze both)

**Input/output in BRDSPI chain:**
- Input: Git URL + optional scope (target directories)
- Output: `.docs/research/` artifact with findings
- Downstream consumers: `/designing-code`, `/structuring-code`, `/planning-code`

## Code References

**Existing research skills (pattern sources):**
- `newskills/researching-code/SKILL.md` (232 lines) — codebase agent spawning pattern
- `newskills/researching-code/reference/research-agents.md` (71 lines) — agent catalog
- `newskills/researching-code/reference/evidence-requirements.md` (65 lines) — evidence standards
- `newskills/researching-code/templates/research-document-template.md` (85 lines) — output template
- `newskills/researching-web/SKILL.md` (268 lines) — web research pattern
- `newskills/researching-web/reference/search-strategies.md` (124 lines) — decomposition patterns
- `newskills/researching-web/reference/evidence-requirements.md` (92 lines) — source quality
- `newskills/researching-frameworks/SKILL.md` (295 lines) — MCP + web fallback pattern
- `newskills/researching-frameworks/reference/context7-usage.md` (117 lines) — tool detection
- `newskills/researching-frameworks/reference/research-tiers.md` (108 lines) — tier classification

**Initialization pattern source:**
- `newskills/starting-projects/SKILL.md` (214 lines) — AskUserQuestion interaction pattern
- `newskills/starting-projects/reference/question-design.md` (56 lines) — question design

**CLAUDE.md/AGENTS.md context:**
- `newskills/updating-claude-md/SKILL.md` — scope detection (global vs project)
- `.docs/research/01-28-2026-anthropic-skills-repo.md` — skills repo example
- `.docs/research/01-28-2026-claude-reflect-repo.md:316-327` — AGENTS.md format

**docs-writer integration:**
- `newagents/docs-writer.md` — agent specification with input contract
- All research skills' write steps — consistent Task prompt format

**Concept and roadmap:**
- `.docs/future-skills/researching-repo.md` — original concept document
- `.docs/plans/02-07-2026-future-skills-implementation-roadmap.md:254-278` — Phase 3 requirements
- `.docs/research/02-07-2026-phase-2-brdspi-core-research.md` — Phase 2 precedent

## Architecture Notes

### Pattern: Research Skill Template

All research skills share an identical structural template:
```
Frontmatter → Iron Law → Gate Function → Initial Response → Process Steps →
Important Guidelines → Red Flags → Rationalization Prevention → Bottom Line
```

`/researching-repo` must follow this exact structure with domain-specific content.

### Pattern: Clone-as-Workspace

Unlike other research skills that operate on existing content (the current project, the web, or MCP tools), `/researching-repo` must first **create** its workspace by cloning, then operate on it, then **destroy** it. This introduces a lifecycle management concern unique to this skill.

The lifecycle is: CLONE → SECURE → ANALYZE → PERSIST → CLEANUP

This maps to the Gate Function as additional pre-analysis steps that other research skills don't need.

### Pattern: Agent Context Switching

When spawning codebase analysis agents (code-locator, code-analyzer, code-librarian), `/researching-repo` must pass the **clone directory path** as the working context, not the current project. This is critical — agents must analyze the cloned repo, not the user's project.

The Task tool's prompt must explicitly state the path to analyze:
```
"Analyze the repository cloned at {clone_dir}. Focus on..."
```

### Pattern: Scoped Analysis

The concept doc mentions scoped analysis: "just look at `src/skills/`". This is similar to how `/researching-code` allows specific questions about specific areas, but with the added constraint that the scope refers to paths within the cloned repo, not the current project.

### Security Architecture

`/researching-repo` is the only skill that executes operations on untrusted external content. The security model is:
1. **Prevention** — disable symlinks, hooks, submodules during clone
2. **Verification** — check for hooks after clone
3. **Isolation** — temp directory, no checkout by default
4. **Cleanup** — automatic deletion via trap

## Open Questions

1. **Blobless vs shallow for local paths?** — `--filter=blob:none` requires server support. Local repos may not support it. Should the skill detect local paths and fall back to `--depth=1`?

2. **Sparse checkout for scoped analysis?** — When the user targets a specific subdirectory, should the skill use sparse checkout to only fetch that subtree? Or analyze from `git ls-tree` without checkout?

3. **Multiple repos in one session?** — The concept doc mentions "clone two competing projects, analyze both, produce comparison." Should this be a separate mode, or should the user invoke the skill twice and synthesize manually?

4. **Reusable "patterns" artifact format?** — The concept doc asks if output could produce something `/designing-code` or `/structuring-code` can reference. What format should this take? Same `.docs/research/` file, or a separate `.docs/patterns/` artifact?

5. **Agent working directory on Windows** — Can Task agents be directed to operate on the clone path via their prompt alone, or do they need a path parameter? Need to verify during implementation.

6. **Authentication failure UX** — When cloning a private repo fails due to auth, should the skill offer SSH/HTTPS alternatives, or just report the failure and let the user fix it?
