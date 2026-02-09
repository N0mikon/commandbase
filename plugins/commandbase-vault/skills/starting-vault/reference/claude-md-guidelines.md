# Vault CLAUDE.md Guidelines

Guidelines for creating vault-aware CLAUDE.md files.

## Core Principles

1. **Less is more** - Under 60 lines ideal, never exceed 300
2. **Universally applicable** - Only info relevant to EVERY vault session
3. **Progressive disclosure** - Point to .docs/ artifacts, don't inline everything
4. **Vault-specific** - Include vault path, MCP config, and vault conventions
5. **No API keys** - Never include secrets in CLAUDE.md

## Vault-Specific Sections

A vault CLAUDE.md includes sections not found in code project CLAUDE.md files:

### Vault Identity
- Vault path on disk
- Vault purpose (one sentence)
- Organization philosophy (from brainstorm artifact if available)

### MCP Connection
- Which MCP server is configured
- Base URL (but NOT the API key)
- Available MCP tools for this vault

### Vault Conventions
- Folder structure overview
- Naming conventions
- Frontmatter schema (if standardized)
- Tag taxonomy summary
- Link format (wikilinks vs markdown)

### Verification
- MCP connectivity test command description
- How to verify vault access is working

## What NOT to Include

- API keys or secrets (use environment variables)
- Detailed plugin configuration (belongs in .docs/)
- Full tag taxonomy (point to design doc)
- Complete frontmatter schema (point to design doc)
- Note templates (those go in vault templates/ folder)
- Global Claude rules (inherited from ~/.claude/CLAUDE.md)

## Hierarchy Awareness

Vault CLAUDE.md inherits from global (`~/.claude/CLAUDE.md`).

**Don't duplicate:**
- Security NEVER rules (defined globally)
- Git safety rules (defined globally)
- Commit workflow rules (defined globally)

**Do include:**
- Vault-specific path and purpose
- MCP connection details (minus API key)
- Vault conventions and structure
- Pointers to vault .docs/ artifacts
