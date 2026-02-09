# Services Research Template

Template for infrastructure research findings written to `.docs/research/`.

## File Naming

Format: `MM-DD-YYYY-description.md` in `.docs/research/`

Examples:
- `02-08-2026-homelab-infrastructure-audit.md`
- `02-08-2026-media-stack-port-mapping.md`
- `02-08-2026-backup-coverage-analysis.md`

## Frontmatter

Handled by docs-writer agent. Provide these fields:
```yaml
doc_type: "research"
topic: "<infrastructure research topic>"
tags: [services, <relevant aspect tags>]
references: [<key compose files, config files discovered>]
```

## Body Sections

```markdown
# <Research Topic>

**Date**: YYYY-MM-DD
**Repo Path**: <homelab_repo_path or current directory>

## Research Question

<The specific question being investigated>

## Summary

<2-4 sentence overview of key findings>

## Infrastructure Overview

- **Services**: <count> services across <count> compose file(s)
- **Networks**: <count> Docker networks
- **Volumes**: <count> named volumes, <count> bind mounts
- **Proxy Routes**: <count> routed domains/paths
- **Backup Coverage**: <percentage or description>

## Detailed Findings

### Service Inventory

| Service | Image | Version | Restart Policy | Compose File |
|---------|-------|---------|----------------|-------------|
| ... | ... | ... | ... | ... |

### Port Mapping

| Service | Host Port | Container Port | Protocol | Notes |
|---------|-----------|----------------|----------|-------|
| ... | ... | ... | ... | ... |

### Network Topology

<Network map or table showing service-to-network assignments>

### Volume Mapping

| Service | Type | Host Path | Container Path | Read-Only |
|---------|------|-----------|----------------|-----------|
| ... | ... | ... | ... | ... |

### Environment Config

| Service | .env Location | Variables (names only) | .env.example Exists |
|---------|--------------|----------------------|---------------------|
| ... | ... | ... | ... |

### Reverse Proxy Routes

| Domain/Path | Target Service | SSL | Middleware |
|-------------|---------------|-----|-----------|
| ... | ... | ... | ... |

### Dependencies

<Dependency graph or table showing startup order and health checks>

### Backup Coverage

| What | Tool | Schedule | Destination | Retention |
|------|------|----------|-------------|-----------|
| ... | ... | ... | ... | ... |

### Resource Usage

| Service | Memory Limit | CPU Limit | Actual Usage |
|---------|-------------|-----------|-------------|
| ... | ... | ... | ... |

## Gaps & Risks

| Severity | Issue | Affected Services | Details |
|----------|-------|-------------------|---------|
| Critical | ... | ... | ... |
| Warning | ... | ... | ... |
| Info | ... | ... | ... |

## File References

<Deduplicated list of all files examined during research>

## Architecture Notes

<Observed patterns, conventions, and organizational decisions>

## Open Questions

<Areas needing further investigation or user clarification>
```

## Section Guidelines

- **Infrastructure Overview**: Always include service/network/volume counts for quick reference
- **Detailed Findings**: Include only dimensions relevant to the research question; omit empty sections
- **Environment Config**: Variable NAMES only, NEVER values. Note whether .env.example exists
- **Gaps & Risks**: Only include if the research question calls for gap analysis or if critical issues are discovered
- **File References**: Every finding must trace back to a specific file path
- **Open Questions**: Items that need user input or live-state verification
