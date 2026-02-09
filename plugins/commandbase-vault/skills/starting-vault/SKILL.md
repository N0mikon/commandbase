---
name: starting-vault
description: "Use this skill when initializing a new Obsidian vault for Claude Code management or configuring Claude Code to work with an existing vault. This includes discovering vault path, configuring MCP server connection, setting up API key, creating vault-aware CLAUDE.md, and testing MCP connectivity. Activate when the user says 'start a vault', 'set up vault', 'configure obsidian', 'connect to vault', or before running vault BRDSPI."
---

# Starting Vault

You are tasked with helping initialize an Obsidian vault for Claude Code management. This skill guides the user through vault discovery, MCP server configuration, connectivity testing, and generating a vault-aware CLAUDE.md file.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO VAULT SETUP WITHOUT TESTING CONNECTIVITY FIRST
```

Don't declare setup complete without verifying MCP connectivity to the vault.

**No exceptions:**
- Don't skip connectivity testing for "simple" vaults — broken MCP config wastes every downstream step
- Don't assume the vault path is correct — verify it exists and is accessible
- Don't recommend an MCP server without explaining trade-offs
- Don't create CLAUDE.md before connectivity is confirmed

## The Gate Function

```
BEFORE declaring vault setup complete:

1. DISCOVER: Vault path, existing or new, MCP server preference
2. CONFIGURE: MCP server setup (API key, base URL, server choice)
3. TEST: Verify MCP connectivity (list vault root, read a note)
4. CREATE: Vault-aware CLAUDE.md with vault path, MCP config, verification commands
5. PRESENT: Summary with workflow chain and next steps

Skip connectivity test = setup that may not work
```

## Initial Response

When this skill is invoked, respond with:
```
Welcome! I'll help you set up Claude Code to work with your Obsidian vault.

Let me ask a few questions to understand your setup.
```

Then immediately use the AskUserQuestion tool to gather vault information.

## Phase 1: Vault Discovery

Use the AskUserQuestion tool to ask about the vault. Ask 2-3 questions at a time.

### Round 1: Core Information
- **Vault status**: Is this an existing vault or a new one? (Existing vault, New vault)
- **Vault path**: Where is the vault located on disk? (User provides path)
- **Vault purpose**: What is this vault for? (Personal knowledge, Project docs, Research, Second brain)

### Round 2: MCP Configuration
Based on Round 1 answers, ask about:
- **Obsidian REST API**: Is the Obsidian Local REST API plugin installed? (Yes, No, Not sure)
- **MCP server preference**: Which MCP server to use? (See ./reference/mcp-setup-guide.md for options)

### Round 3: Existing Vault Context (if existing vault)
- **Current organization**: How is the vault currently organized? (PARA, Zettelkasten, Flat, Custom)
- **Brainstorm artifacts**: Have you run /brainstorming-vault already? (Yes with path, No)

**Important**: Adapt questions based on previous answers. Skip irrelevant questions. If user has already run /brainstorming-vault, read that artifact for vault philosophy context.

## Phase 2: MCP Configuration

Guide the user through MCP server setup. See ./reference/mcp-setup-guide.md for detailed steps.

1. **Ensure Obsidian Local REST API plugin is installed and configured**:
   - Plugin must be installed in the vault
   - API key must be generated
   - Default base URL: `http://127.0.0.1:27124`

2. **Configure MCP server**:
   - Help user add the chosen MCP server to their Claude Code MCP configuration
   - Set environment variables: `OBSIDIAN_API_KEY`, `OBSIDIAN_BASE_URL`
   - Present the configuration for the user to add

3. **Present configuration**:
   ```
   MCP Configuration:

   Server: [chosen server]
   Base URL: [base URL]
   API Key: Set via OBSIDIAN_API_KEY environment variable

   Please add this to your MCP configuration and confirm when ready.
   ```

## Phase 3: Connectivity Test

After MCP configuration is confirmed:

1. **Test vault access**: Use MCP tools to list the vault root directory
2. **Test note read**: Use MCP tools to read an existing note (or create a test note)
3. **Report results**:
   ```
   Connectivity Test Results:
   - Vault root listing: [PASS/FAIL]
   - Note read: [PASS/FAIL]

   [If FAIL: troubleshooting steps from ./reference/mcp-setup-guide.md]
   ```

If tests fail, troubleshoot using the guide before proceeding. Do NOT proceed to CLAUDE.md creation with failed connectivity.

## Phase 4: Create CLAUDE.md

Generate a vault-aware CLAUDE.md using the template at ./templates/vault-claude-md-template.md.

For detailed guidelines on what to include and exclude, see ./reference/claude-md-guidelines.md.

**Key vault-specific sections:**
- Vault path and purpose
- MCP connection details (server, base URL — NOT the API key)
- Vault verification commands (MCP list root, read a note)
- Vault conventions (from brainstorm artifact if available)
- Pointer to vault BRDSPI workflow

## Phase 5: Wrap Up

After creating CLAUDE.md:

```
Your vault is configured!

**Created:**
- `CLAUDE.md` - Vault-aware project configuration

**Verified:**
- MCP connectivity: [server name] connected to [vault path]
- Vault root accessible via MCP tools

**Next steps:**
1. Review CLAUDE.md and make any manual adjustments
2. If you haven't already: /brainstorming-vault to settle vault philosophy
3. /researching-vault to analyze current vault structure
4. /designing-vault to make organizational decisions
5. /structuring-vault to map folder layout
6. /planning-vault to create implementation plan
7. /implementing-vault to execute vault changes

**Your vault BRDSPI workflow:**
/brainstorming-vault → /starting-vault → /researching-vault → /designing-vault → /structuring-vault → /planning-vault → /implementing-vault
```

## Important Guidelines

1. **Be conversational**: This is a collaborative process, not a form to fill out
2. **Adapt dynamically**: Skip questions that don't apply, add questions when needed
3. **Test before declaring success**: MCP connectivity must be verified
4. **Keep CLAUDE.md minimal**: Under 60 lines, vault-specific info only
5. **Respect existing setup**: If vault has conventions, capture them in CLAUDE.md

## Red Flags - STOP and Verify

If you notice any of these, pause:

- Declaring setup complete without running connectivity test
- Writing CLAUDE.md over 60 lines
- Including the API key in CLAUDE.md or any committed file
- Skipping user confirmation at major decision points
- Assuming MCP server choice without presenting options
- Proceeding past failed connectivity test

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "MCP is probably configured correctly" | Test it. Probably isn't evidence. |
| "User seems in a hurry" | Bad MCP config wastes every downstream step. Test first. |
| "CLAUDE.md needs more vault context" | 60 lines max. Move details to .docs/ if needed. |
| "This vault is simple, skip discovery" | Simple vaults still need MCP config and CLAUDE.md. |
| "I'll test connectivity later" | Test now. Everything downstream depends on it. |

## The Bottom Line

**Interactive, but principled.**

Discover vault needs. Configure MCP. Test connectivity. Create minimal CLAUDE.md. Confirm everything works.

This is non-negotiable. Every vault. Every time.
