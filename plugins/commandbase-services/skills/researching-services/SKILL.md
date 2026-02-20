---
name: researching-services
description: "Use this skill when researching homelab or Docker service infrastructure to understand current state. This includes mapping running services, port allocations, network topology, volume mounts, environment configuration, reverse proxy routes, service dependencies, backup coverage, and identifying gaps or risks. Activate when the user says 'research services', 'map infrastructure', 'what services are running', 'analyze homelab', or before designing infrastructure changes with /designing-services."
---

# Researching Services

You are tasked with conducting comprehensive research across homelab service infrastructure to answer user questions by exploring repo files and optionally live Docker state, then synthesizing findings into a research document.

**Violating the letter of these rules is violating the spirit of these rules.**

## Your Role

Document and explain the infrastructure as it exists today:
- Describe what exists, where it exists, how services connect, and how they're configured
- Create a technical map/documentation of the existing infrastructure
- Do NOT suggest improvements or changes unless explicitly asked
- Do NOT critique the organization or identify problems
- Only describe the current state

## The Iron Law

```
NO SYNTHESIS WITHOUT INFRASTRUCTURE EXPLORATION FIRST
```

If you haven't explored the repo files and examined the results, you cannot synthesize findings.

**No exceptions:**
- Don't answer from assumptions - explore the repo files to verify
- Don't skip exploration for "simple" setups - simple setups have hidden dependencies
- Don't synthesize partial results - complete all exploration before reporting
- Don't guess at service topology - use tools to discover it

## The Gate Function

```
BEFORE completing research:

1. CONFIGURE: Check CLAUDE.md for `homelab_repo_path`; if not found, check current directory for compose files
2. IDENTIFY: What aspects of the infrastructure need investigation?
3. EXPLORE: Use file-system Glob/Grep/Read to map repo structure (compose files, configs, .env.example)
4. LIVE STATE (optional): If `homelab_same_machine: true`, run read-only docker commands; otherwise ask user to provide output
5. ANALYZE: Cross-reference repo files with live state; identify gaps
6. WRITE: Create .docs/research/MM-DD-YYYY-description.md via docs-writer (MANDATORY)
7. PRESENT: Summary to user with link to research file

Skipping steps = incomplete research
Research without a file = research that will be lost
```

## Initial Response

When this skill is invoked:

1. **If a specific question or area was provided**, begin research immediately
2. **If no parameters provided**, respond with:
```
I'm ready to research your homelab service infrastructure. Please provide your research question or area of interest, and I'll analyze it thoroughly by exploring compose files, configs, networking, and service topology.

Examples:
- "What services are running and how are they connected?"
- "Map the port allocations across all services"
- "What's the backup coverage for critical data?"
- "Document the reverse proxy routing setup"
- "Find services without health checks"
```

Then wait for the user's query.

## Research Process

### Step 1: Read Homelab Configuration

- Read CLAUDE.md for `homelab_repo_path` and `homelab_same_machine` settings
- Check for existing `.docs/research/` artifacts about this infrastructure topic (avoid re-researching)
- Note the repo path and any documented conventions

### Step 2: Decompose Research Question

Break down the query into infrastructure research aspects. See `./reference/services-research-aspects.md` for the full guide on research dimensions.

Common dimensions:
- **Service Inventory**: Running services, images, versions from compose files
- **Port Mapping**: Host:container port bindings and conflicts
- **Network Topology**: Docker networks and inter-service connectivity
- **Volume Mapping**: Bind mounts, named volumes, data locations
- **Environment Config**: .env file locations, variable NAMES (never values)
- **Reverse Proxy Routes**: Domains, paths, SSL, middleware
- **Dependencies**: Startup order, health checks, shared databases
- **Backup Coverage**: What's backed up, schedule, destinations
- **Resource Usage**: CPU/memory limits and actual usage
- **Gaps & Risks**: Missing backups, exposed ports, no health checks

### Step 3: Explore Repo Files

Explore the homelab repo using file-system tools:

- Find compose files: `Glob("**/docker-compose*.yml", path=repo_path)` and `Glob("**/compose*.yml", path=repo_path)`
- Find config files: `Glob("**/*.conf", path=repo_path)`, `Glob("**/*.toml", path=repo_path)`, `Glob("**/*.yml", path=repo_path)`
- Find .env examples: `Glob("**/.env.example", path=repo_path)`, `Glob("**/.env.sample", path=repo_path)`
- Search for ports: `Grep("ports:", path=repo_path, glob="*.yml")`
- Search for networks: `Grep("networks:", path=repo_path, glob="*.yml")`
- Search for volumes: `Grep("volumes:", path=repo_path, glob="*.yml")`
- Read proxy configs: Traefik labels, nginx configs, Caddy files

For complex infrastructure, spawn `general-purpose` agents to explore different aspects in parallel (compose files, proxy configs, backup configs, .env.example files).

**Secrets handling:** When encountering .env files, document file LOCATIONS and variable NAMES only. NEVER read .env file contents. Only read .env.example or .env.sample files.

### Step 4: Gather Live State (Optional)

**If `homelab_same_machine: true` in CLAUDE.md:**
- Run read-only docker commands: `docker ps --format`, `docker network ls`, `docker volume ls`, `docker stats --no-stream`
- Cross-reference live state with repo files

**If not same-machine or not set:**
- Present commands for user to run and provide output:
```
To complete the research, please run these commands and share the output:
- `docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"`
- `docker network ls`
- `docker volume ls`
```

### Step 5: Cross-Reference and Identify Gaps

After ALL exploration is complete:
- Compare compose definitions with live state (if available)
- Identify port conflicts or overlapping allocations
- Find services without health checks
- Find volumes not covered by backup configs
- Note services exposed without reverse proxy protection

### Step 6: Write Research Document

Spawn a `docs-writer` agent via the Task tool to create the research file:

```
Task prompt:
  doc_type: "research"
  topic: "<infrastructure research topic>"
  tags: [services, <relevant aspect tags>]
  references: [<key compose files, config files discovered>]
  content: |
    <compiled findings using ./templates/services-research-template.md>
```

The agent handles frontmatter, file naming, and directory creation.

### Step 7: Present Findings

- Present a concise summary to the user
- Include key file references for easy navigation
- Ask if they have follow-up questions

## Important Guidelines

1. **Document, Don't Evaluate**
   - Describe what IS, not what SHOULD BE
   - No recommendations unless asked
   - No critiques or "improvements"

2. **Be Thorough**
   - Explore multiple infrastructure dimensions
   - Always include file path references
   - Connect related findings (e.g., port mapping + proxy routes)

3. **Be Accurate**
   - Verify findings against actual repo files via tools
   - Don't guess - explore to investigate
   - Every claim needs a file path or config reference
   - Note uncertainties clearly and explore further

4. **Protect Secrets**
   - NEVER read .env file contents
   - Document variable NAMES from .env.example only
   - Never include secret values in research output

5. **Stay Focused**
   - Answer the specific question asked
   - Don't go on tangents
   - Keep the research scoped

## Self-Improvement

Before finishing, review this skill execution:

- If errors occurred (tool failures, skill failures, repeated attempts), suggest:
  > **Suggestion**: [N] errors occurred during this execution.
  > Consider running `/extracting-patterns` to capture learnings.
  >
  > Errors: [brief summary of error types]
- Only suggest when errors are meaningful — use judgment about significance.
- Do not auto-run. Suggest only.

## Red Flags - STOP and Verify

If you notice any of these, pause:

- Presenting findings without creating a research file first
- Saying "I'll document this later" or "if you want I can save this"
- Completing research without a `.docs/research/` file path in your response
- Skipping the research file because "it was a simple question"
- Synthesizing without exploring the repo files first
- Reading .env file contents instead of .env.example
- Including secret values in research output

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "It was a quick answer, no file needed" | Every research produces a file. No exceptions. |
| "I'll create the file if they ask" | Create it first. They shouldn't have to ask. |
| "I just need to peek at the .env file" | Read .env.example. Never .env contents. |
| "I already presented the findings" | File comes BEFORE presentation, not after. |
| "There wasn't much to document" | Short findings = short file. Still required. |

## The Bottom Line

**No shortcuts for research.**

Explore the repo. Verify with tools. Cite file references. Protect secrets. Write the research file. THEN present findings.

This is non-negotiable. Every question. Every time.
