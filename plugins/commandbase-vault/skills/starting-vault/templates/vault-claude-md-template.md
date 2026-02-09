# Vault CLAUDE.md Template

Use this template when generating a vault-aware CLAUDE.md file.

## Principles

- **Less is more**: Keep under 60 lines if possible, never exceed 300 lines
- **Vault-specific**: Include vault path, MCP config, conventions
- **No secrets**: Never include API keys — use environment variables
- **Progressive disclosure**: Point to .docs/ artifacts for details

## Template

````markdown
# [Vault Name]

[One sentence: what this vault is for]

## Vault Path

`[/absolute/path/to/vault]`

## MCP Connection

- **Server**: [MCP server name]
- **Base URL**: [http://127.0.0.1:27124 or custom]
- **Tools available**: [list key MCP tools: read, write, search, etc.]

## Vault Structure

```
[Brief folder layout - top-level directories only]
```

## Vault Conventions

- **Link format**: [Wikilinks / Markdown links]
- **Naming**: [Descriptive titles / ID-prefixed / etc.]
- **Frontmatter**: [Minimal / Rich — point to design doc for schema]
- **Tags**: [Flat / Hierarchical — point to design doc for taxonomy]

## Verification

To verify vault connectivity:
- List vault root via MCP list tool
- Read any note via MCP read tool

## Additional Context

For detailed documentation, see:
- `.docs/brainstorm/` - Vault philosophy decisions
- `.docs/design/` - Vault design decisions (MOCs, tags, templates)
- `.docs/structure/` - Vault structural map

## Vault BRDSPI Workflow

- `/brainstorming-vault` - Explore vault philosophy
- `/researching-vault` - Analyze vault structure
- `/designing-vault` - Make organizational decisions
- `/structuring-vault` - Map folder layout
- `/planning-vault` - Create implementation plan
- `/implementing-vault` - Execute vault changes
- `/importing-vault` - Convert .docs/ to vault notes
````

## Generation Process

1. **Draft the CLAUDE.md** based on discovery answers:
   - Extract vault identity (name, path, purpose)
   - Include MCP connection details (minus API key)
   - Capture vault conventions (from brainstorm artifact if available)
   - Add verification steps

2. **Review for conciseness**:
   - Remove anything not universally applicable to vault sessions
   - Remove detailed schemas (use progressive disclosure)
   - Ensure under 60 lines

3. **Present for approval**:
   ```
   Here's your vault CLAUDE.md. I've kept it concise and vault-focused:

   [Show the content]

   Key principles applied:
   - [X] Under 60 lines
   - [X] No API keys (stored in environment variables)
   - [X] Pointers to .docs/ artifacts for details
   - [X] MCP connectivity verification steps

   Want me to adjust anything?
   ```

4. **Write the file** after approval

## What NOT to Include

See ./reference/claude-md-guidelines.md for the full list of anti-patterns.
