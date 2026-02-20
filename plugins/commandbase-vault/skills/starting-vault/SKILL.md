---
name: starting-vault
description: "Use this skill when initializing a new Obsidian vault for Claude Code management or configuring Claude Code to work with an existing vault. This includes discovering vault path, choosing an access method (filesystem or MCP), configuring connectivity, supporting multi-vault setups, creating vault-aware CLAUDE.md, and verifying access. Activate when the user says 'start a vault', 'set up vault', 'configure obsidian', 'connect to vault', or before running vault workflows."
---

# Starting Vault

You are tasked with helping initialize an Obsidian vault for Claude Code management. This skill guides the user through vault discovery, MCP server configuration, connectivity testing, and generating a vault-aware CLAUDE.md file.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO VAULT SETUP WITHOUT VERIFYING ACCESS FIRST
```

Don't declare setup complete without verifying Claude Code can access the vault — whether via filesystem, MCP, or both.

**No exceptions:**
- Don't skip access verification for "simple" vaults — broken access wastes every downstream step
- Don't assume the vault path is correct — verify it exists and is accessible
- Don't recommend an access method without explaining trade-offs
- Don't create CLAUDE.md before access is confirmed

## The Gate Function

```
BEFORE declaring vault setup complete:

1. DISCOVER: Vault path, existing or new, single or multi-vault
2. CHOOSE ACCESS PATH: Filesystem only, or filesystem + MCP
3. CONFIGURE: MCP server setup if chosen (skip if filesystem-only)
4. TEST: Verify access (filesystem: vault path exists; MCP: connectivity test)
5. CREATE: Vault-aware CLAUDE.md adapted to access path
6. PRESENT: Summary with workflow chain and next steps

Skip access verification = setup that may not work
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
- **Multi-vault**: Do you have multiple vaults? (Single vault, Multiple vaults)
  - If multiple: Ask about shared conventions, unique MCP ports per vault, vault boundary rules

### Round 2: Access Path
Based on Round 1 answers, ask about access method:
- **Access method**: How should Claude Code access the vault?
  - "Filesystem only (no plugins needed, works immediately)" — Claude reads/writes vault files directly
  - "Filesystem + MCP (adds search and metadata tools, requires Obsidian Local REST API plugin)" — filesystem as primary, MCP for semantic search and plugin features

### Round 3: Existing Vault Context (if existing vault)
- **Current organization**: How is the vault currently organized? (PARA, Zettelkasten, Flat, Custom)
- **Brainstorm artifacts**: Have you run /brainstorming-vault already? (Yes with path, No)

**Important**: Adapt questions based on previous answers. Skip irrelevant questions. If user has already run /brainstorming-vault, read that artifact for vault philosophy context.

## Phase 2: MCP Configuration (if MCP chosen)

**Skip this phase if the user chose filesystem-only access.** Proceed directly to Phase 3.

If MCP was chosen, guide the user through setup. See ./reference/mcp-setup-guide.md for detailed steps (note: this guide only applies when MCP path is chosen).

1. **Ensure Obsidian Local REST API plugin is installed and configured**:
   - Plugin must be installed in the vault
   - API key must be generated
   - Default base URL: `http://127.0.0.1:27124`
   - For multi-vault setups: each vault needs a unique port

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

## Phase 3: Access Verification

Test the chosen access path to verify Claude Code can reach the vault.

**Filesystem-only path:**
1. **Test vault path**: Verify vault directory exists via `Glob("*.md", path=vault_path)`
2. **Test note read**: Read any existing .md file in the vault
3. **Report results**:
   ```
   Filesystem Access Test:
   - Vault path exists: [PASS/FAIL]
   - Note read: [PASS/FAIL]
   ```

**Filesystem + MCP path:**
1. **Test filesystem access**: Same as above
2. **Test MCP connectivity**: Use MCP tools to list the vault root directory
3. **Test MCP note read**: Use MCP tools to read an existing note
4. **Report results**:
   ```
   Access Test Results:
   - Filesystem vault path: [PASS/FAIL]
   - MCP vault root listing: [PASS/FAIL]
   - MCP note read: [PASS/FAIL]

   [If MCP FAIL: troubleshooting steps from ./reference/mcp-setup-guide.md]
   ```

If tests fail, troubleshoot before proceeding. Do NOT proceed to CLAUDE.md creation with failed access.

## Phase 4: Create CLAUDE.md

Generate a vault-aware CLAUDE.md using the template at ./templates/vault-claude-md-template.md.

For detailed guidelines on what to include and exclude, see ./reference/claude-md-guidelines.md.

**Key vault-specific sections:**
- Vault path and purpose
- Access method (filesystem-only or filesystem + MCP)
- MCP connection details if applicable (server, base URL — NOT the API key)
- Vault verification commands (adapted to access path)
- Vault conventions (from brainstorm artifact if available)
- Pointer to vault BRDSPI workflow and operations skills

## Phase 5: Wrap Up

After creating CLAUDE.md:

```
Your vault is configured!

**Created:**
- `CLAUDE.md` - Vault-aware project configuration

**Verified:**
- Access path: [filesystem-only / filesystem + MCP]
- Vault path accessible: [vault path]
[If MCP: - MCP connectivity: [server name] connected]

**Construction workflow (BRDSPI):**
1. /brainstorming-vault — settle vault philosophy
2. /researching-vault — analyze current vault structure
3. /designing-vault — make organizational decisions
4. /structuring-vault — map folder layout
5. /planning-vault — create implementation plan
6. /implementing-vault — execute vault changes

**Daily operations:**
- /reviewing-vault — daily, weekly, or monthly vault reviews
- /capturing-vault — quick note creation from various sources
- /connecting-vault — discover relationships, maintain MOCs

**Maintenance:**
- /linting-vault — vault health checks and validation
- /maintaining-vault — batch tag, frontmatter, and cleanup operations
```

## Important Guidelines

1. **Be conversational**: This is a collaborative process, not a form to fill out
2. **Adapt dynamically**: Skip questions that don't apply, add questions when needed
3. **Test before declaring success**: Vault access must be verified (filesystem or MCP)
4. **Keep CLAUDE.md minimal**: Under 60 lines, vault-specific info only
5. **Respect existing setup**: If vault has conventions, capture them in CLAUDE.md

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

- Declaring setup complete without running access verification
- Writing CLAUDE.md over 60 lines
- Including the API key in CLAUDE.md or any committed file
- Skipping user confirmation at major decision points
- Assuming access method without presenting options
- Proceeding past failed access verification

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Access is probably working" | Test it. Probably isn't evidence. |
| "User seems in a hurry" | Bad access config wastes every downstream step. Test first. |
| "CLAUDE.md needs more vault context" | 60 lines max. Move details to .docs/ if needed. |
| "This vault is simple, skip discovery" | Simple vaults still need access verification and CLAUDE.md. |
| "I'll test access later" | Test now. Everything downstream depends on it. |

## The Bottom Line

**Interactive, but principled.**

Discover vault needs. Choose access path. Verify access. Create minimal CLAUDE.md. Confirm everything works.

This is non-negotiable. Every vault. Every time.
