# Homelab Services RDSPI Workflow

## Problem

Homelab services (Docker Compose stacks, reverse proxy configs, DNS entries, backup jobs) live in a plan repo but changes are applied ad-hoc. No structured workflow for understanding state, designing changes, and executing with verification.

## Concept

Full RDSPI for infrastructure managed through a plan repo, with `/brainstorming-services` as the pre-step:

```
/brainstorming-services      <- "should I add Authelia or use Cloudflare tunnels?"
  R  /services-research      <- map services, ports, networks, volumes, dependencies, gaps
  D  /services-design        <- stack decisions, networking strategy, auth approach, backup policy
  S  /services-structure     <- which compose files change, env templates, proxy routes, ordering
  P  /services-plan          <- phased tasks with success criteria
  I  /services-implement     <- edit configs, generate deploy commands (pause for user to run)
```

## Services-Specific Considerations

- **Deployment is hands-off** — generate commands/scripts, don't execute directly
- **Secrets handling** — compose files reference `.env` files that shouldn't be read/committed
- **Post-deploy verification** — connectivity checks, log review, backup registration
- The plan repo is already file-based — Claude Code's tools work natively on it

## Open Questions

- How to reference the homelab plan repo? Separate working directory, env var, or CLAUDE.md pointer?
- Should research pull live state (e.g., `docker ps` via SSH) or only analyze repo files?
- Integration with monitoring (Uptime Kuma, Prometheus) for post-deploy verification?
- Does `/starting-refactors` have a services equivalent for infrastructure reorganization?
