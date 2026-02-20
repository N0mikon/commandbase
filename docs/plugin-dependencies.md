# Plugin Dependencies

commandbase-core is the foundation. It exports 4 documentation agents (docs-writer, docs-updater, docs-locator, docs-analyzer) that every other plugin relies on — except commandbase-meta, which stands alone as the skill/agent authoring toolkit.

The three domain plugins (code, vault, services) also cross-reference `/committing-changes` from git-workflow for their commit flows.

```mermaid
flowchart TB
    subgraph foundation["Foundation"]
        core["commandbase-core<br>5 skills · 4 agents"]
    end

    subgraph domain["Domain Plugins"]
        code["commandbase-code<br>8 skills · 3 agents"]
        vault["commandbase-vault<br>8 skills"]
        services["commandbase-services<br>6 skills"]
    end

    subgraph supporting["Supporting Plugins"]
        research["commandbase-research<br>4 skills · 1 agent"]
        git["commandbase-git-workflow<br>5 skills · 1 hook"]
        session["commandbase-session<br>5 skills"]
    end

    meta["commandbase-meta<br>6 skills · standalone"]

    core --> code
    core --> vault
    core --> services
    core --> research
    core --> git
    core --> session

    git -.->|"/committing-changes"| code
    git -.->|"/committing-changes"| vault
    git -.->|"/committing-changes"| services
    git -.->|"/committing-changes"| session
```

## What each plugin exports

| Plugin | Exports | Used by |
|--------|---------|---------|
| core | docs-writer, docs-updater, docs-locator, docs-analyzer, /bookmarking-code, /validating-code, /starting-projects | All except meta |
| git-workflow | /committing-changes, /reviewing-changes, /reviewing-security, /creating-prs, /auditing-docs | code, vault, services, session |
| code | code-analyzer, code-librarian, code-locator | Available to any conversation |
| research | web-researcher | Available to any conversation |
| meta | Standalone — no exports consumed by other plugins | — |

The most-referenced skill across the system is `/committing-changes` — it's invoked by /implementing-plans, /debugging-code, /ending-worktree, /validating-code, /starting-projects, and /reviewing-changes.
