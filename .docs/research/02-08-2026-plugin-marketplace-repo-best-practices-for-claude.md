---
date: 2026-02-08
status: complete
topic: "Plugin Marketplace Repo Best Practices for Claude"
tags: [research, claude-code, plugin-marketplace, skills-sharing, mcp, open-source]
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Updated after 10 commits - refreshed git_commit, added implementation note in Section 8"
---

# Plugin Marketplace Repo Best Practices for Claude

## Research Question
What are the best practices for creating a plugin marketplace repository for Claude Code, including repo structure, metadata standards, submission processes, and distribution patterns?

## Summary
Claude Code now has an **official plugin marketplace system** (launched December 2025) that allows anyone to create and distribute plugin marketplaces via `marketplace.json` files in GitHub repos. The ecosystem is decentralized by design — Anthropic provides infrastructure rather than controlling a single registry. Best practices draw from both the official system and proven patterns from Obsidian, Homebrew, Krew, and the broader MCP registry ecosystem.

## Detailed Findings

### 1. Claude Code's Official Plugin Marketplace System

**Sources:** [Claude Code Docs - Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces), [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)

Anthropic launched the official plugin marketplace in December 2025 with 36 curated plugins. Key architectural decisions:

- **Decentralized model**: Anyone can create and distribute their own marketplace using `marketplace.json`
- **Git-based distribution**: Marketplaces are GitHub repos; users add them via `/plugin marketplace add owner/repo`
- **Multiple source types**: Git repos, local paths, direct URLs
- **Automatic updates and version tracking** built-in
- **Reserved names**: `claude-code-marketplace`, `claude-plugins-official`, `anthropic-marketplace`, etc. are blocked from community use
- **Enterprise support**: `extraKnownMarketplaces`, `strictKnownMarketplaces`, and `enabledPlugins` settings for org control

**Plugin structure**:
```
plugin-name/
├── .claude-plugin/plugin.json    # Manifest
├── .mcp.json                     # MCP tool connections
├── commands/                     # Slash commands (.md files)
└── skills/                       # Domain knowledge (.md files)
```

As of January 2026: **43 total marketplaces with 834 total plugins** across the ecosystem.

### 2. Proven Repo Structure Patterns from Other Ecosystems

**Sources:** [obsidianmd/obsidian-releases](https://github.com/obsidianmd/obsidian-releases), [kubernetes-sigs/krew-index](https://github.com/kubernetes-sigs/krew-index), [Homebrew Taps Docs](https://docs.brew.sh/Taps)

| Pattern | Example | Best For |
|---------|---------|----------|
| Centralized JSON registry | Obsidian `community-plugins.json` | Simple plugin lists, minimal metadata |
| YAML manifest per plugin | Krew `plugins/name.yaml` | Multi-platform, checksums needed |
| Decentralized taps | Homebrew `homebrew-{name}` | Self-publishing, no approval needed |
| File-based directory | Anthropic `knowledge-work-plugins` | Markdown-based plugins |

**Obsidian model** (most relevant to Claude): Single `community-plugins.json` with minimal fields (id, name, author, description, repo). Plugins hosted in separate repos. PR-based submission.

**Krew model** (most rigorous): YAML manifests with semver, SHA256 checksums, platform selectors. Case-by-case PR review with OWNERS governance.

### 3. Metadata Standards

**Sources:** Cross-platform analysis

Common required fields across all successful marketplaces:
- **id/name**: Unique identifier
- **description**: Brief one-sentence summary
- **author**: Creator name/handle
- **version**: Semantic versioning
- **repo/source**: GitHub URL or package identifier

Optional but valuable:
- **tags/categories**: For discovery
- **compatibility**: Min version requirements
- **checksums**: SHA256 for security
- **license**: SPDX identifier

Keep required fields to 4-6 items. Minimal metadata lowers the contribution barrier.

### 4. MCP Registry Ecosystem

**Sources:** [Official MCP Registry](https://registry.modelcontextprotocol.io/), [mcp.so](https://mcp.so/), [Smithery](https://smithery.ai/)

The MCP ecosystem provides a parallel model:
- **Official registry** launched September 2025 (API v0.1) — REST-based, OpenAPI 3.1.0
- **server.json** standard with schema validation, namespace verification (GitHub OAuth, DNS, HTTP)
- **Package registries**: NPM (`mcpName` in package.json), PyPI (mcp-name in README), Docker (label in Dockerfile)
- **Community directories**: mcp.so (17,556 servers), Glama (17,109 servers), Smithery, PulseMCP (8,250+)
- **Publishing CLI**: `mcp-publisher init` → `login github` → `publish`

### 5. Agent Skills Open Standard

**Sources:** [Anthropic - Agent Skills announcement](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills), [SiliconANGLE](https://siliconangle.com/2025/12/18/anthropic-makes-agent-skills-open-standard/)

Anthropic published Agent Skills as an open standard (December 18, 2025) at agentskills.io:
- Skills are **portable across AI platforms** (not just Claude)
- OpenAI adopted structurally identical architecture in ChatGPT and Codex CLI
- Enterprise partners: Atlassian, Figma, Canva, Stripe, Notion, Zapier
- This means marketplace plugins can target multiple platforms

### 6. Community Sharing Patterns

**Sources:** [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) (23.2k stars), [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills), [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)

Current distribution models:
1. **GitHub-first**: Clone repo, copy to `~/.claude/` — still dominant
2. **Awesome lists**: Curated directories with PR-based submission
3. **Plugin marketplace**: `/plugin marketplace add owner/repo` — newest, growing
4. **Project-level `.claude/`**: Committed to repo, team gets it automatically
5. **Dotfiles integration**: chezmoi + age encryption for cross-machine sync
6. **Third-party platforms**: SkillsMP, claudemarketplaces.com

### 7. Quality Control Best Practices

**Sources:** Cross-platform analysis

Quality control hierarchy (highest to lowest control):
1. **Automated CI validation** (JSON schema, YAML lint, checksum verify)
2. **Manual PR review** with CONTRIBUTING.md guidelines
3. **Community curation** via awesome lists and star counts
4. **Decentralized trust** (user discretion)

Recommended repo files:
- `CONTRIBUTING.md` — PR process, plugin requirements
- `CODE_OF_CONDUCT.md` — Community standards
- `CHANGELOG.md` — Keep a Changelog format
- `.github/workflows/validate.yml` — Schema validation CI
- `schema.json` — Plugin manifest validation schema

### 8. Recommended Marketplace Repo Structure

Based on cross-referencing all patterns:

```
my-claude-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace manifest
├── plugins/
│   ├── plugin-name-1/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json       # Plugin manifest
│   │   ├── skills/               # Skill .md files
│   │   ├── commands/             # Slash command .md files
│   │   └── README.md             # Plugin documentation
│   └── plugin-name-2/
│       └── ...
├── .github/
│   ├── workflows/
│   │   └── validate.yml          # CI validation
│   └── PULL_REQUEST_TEMPLATE.md  # Submission template
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
└── README.md
```

> **Implementation note (2026-02-09):** This recommended structure was implemented in the commandbase repo itself via commit `87a19a3` (2026-02-08). The repo now uses an 8-plugin marketplace with domain-based grouping under `plugins/`, each containing `.claude-plugin/plugin.json`, `skills/`, and optional `agents/`, `hooks/`, and `scripts/` directories. The top-level `.claude-plugin/marketplace.json` registers all 8 plugins. This validates the pattern above, with the addition that `agents/`, `hooks/`, and `scripts/` directories are useful alongside `skills/` and `commands/`.

## Source Conflicts

- **Distribution method**: Some community sources still recommend manual file copying while official docs push the marketplace system. The marketplace is the forward-looking approach but manual copying remains more common in practice.
- **Centralized vs decentralized**: Anthropic explicitly chose decentralized (anyone can make a marketplace) while Obsidian and Krew use centralized registries. This means there's no single "official" community marketplace — could be opportunity or fragmentation.
- **Agent Skills portability**: Anthropic claims cross-platform compatibility via the open standard, but practical cross-platform sharing is still early.

## Currency Assessment
- Most recent source: February 2026
- Topic velocity: **fast-moving** — plugin marketplace launched December 2025, ecosystem evolving rapidly
- Confidence in currency: **medium** — core patterns are established but details changing month-to-month

## Open Questions
1. What's the optimal `marketplace.json` schema for a community marketplace? (Official docs may have more details)
2. How do private/enterprise marketplaces handle authentication beyond git credential helpers?
3. What validation should CI run on plugin submissions? (Schema check, security scan, test execution?)
4. Should a marketplace repo host plugin code or just reference external repos (Obsidian model)?
5. How will the Agent Skills open standard affect marketplace design going forward?
6. What's the recommended approach for plugin versioning and breaking changes?
