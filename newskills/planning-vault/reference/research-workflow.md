# Vault Research Workflow

Detailed process for researching the vault before writing implementation plans.

## Step 1: Context Gathering & Initial Analysis

1. **Read all mentioned files immediately and FULLY**:
   - Research documents (`.docs/research/` with vault tags)
   - Design documents (`.docs/design/` with vault tags)
   - Structure documents (`.docs/structure/` with vault tags)
   - Vault CLAUDE.md for vault path and MCP config
   - **IMPORTANT**: Read files FULLY without limit/offset parameters
   - **CRITICAL**: DO NOT spawn sub-tasks before reading context files yourself

### Upstream BRDSPI Artifacts

If structural map or design doc is provided as input:
- Read the structural map FULLY — this replaces vault exploration for structure
- Read the referenced design doc FULLY — this provides decision context
- Research scope narrows to: verifying current vault state, confirming note locations, checking for changed content
- Do NOT re-research topics already covered in design/structure docs

2. **Explore the vault to gather context**:
   Use MCP tools and/or file-system tools to verify vault state:

   - **MCP list** or **Glob** to find notes in affected areas
   - **MCP search** or **Grep** to find wikilink references
   - **MCP read** or **Read** to inspect specific notes

   These explorations will:
   - Verify current folder structure
   - Find notes that will be affected
   - Identify wikilink references that need updating
   - Return specific note paths as references

3. **Read all notes identified during exploration**:
   - After exploration completes, read key notes FULLY
   - This ensures you understand content before proposing changes

4. **Analyze and verify understanding**:
   - Cross-reference requirements with actual vault state
   - Identify discrepancies or misunderstandings
   - Note assumptions that need verification
   - Determine true scope based on vault reality

5. **Present informed understanding and focused questions**:
   ```
   Based on the requirements and my vault exploration, I understand we need to [summary].

   I've found that:
   - [Current vault detail with note/folder reference]
   - [Relevant pattern or convention discovered]
   - [Potential complexity or edge case]

   Questions that my exploration couldn't answer:
   - [Specific question requiring user input]
   ```

   Only ask questions that you genuinely cannot answer through vault exploration.

## Step 2: Deep Research & Discovery

After getting initial clarifications:

1. **If the user corrects any misunderstanding**:
   - DO NOT just accept the correction
   - Explore further to verify
   - Only proceed once you've verified the facts yourself

2. **Explore comprehensively**:
   - For complex vault changes, spawn `general-purpose` agents to explore different vault areas in parallel
   - Each agent should use MCP tools or file-system tools for specific exploration tasks

3. **Wait for ALL exploration to complete** before proceeding

4. **Present findings and options**:
   ```
   Based on my exploration, here's what I found:

   **Current State:**
   - [Key discovery about vault structure]
   - [Pattern or convention to follow]

   **Approach Options:**
   1. [Option A] - [pros/cons]
   2. [Option B] - [pros/cons]

   **Open Questions:**
   - [Uncertainty about vault state]

   Which approach aligns best with your goals?
   ```

## Exploration Best Practices

When exploring the vault:

1. **Use the right tool for each operation**:
   - MCP tools for search, metadata, tag operations
   - File-system Glob for finding files by pattern
   - File-system Grep for finding content patterns
   - File-system Read for inspecting specific notes

2. **Verify, don't assume**:
   - Check that folders exist before planning moves into them
   - Verify wikilink targets exist before assuming they do
   - Count notes in folders rather than guessing

3. **Explore affected areas**:
   - Find all notes that link to notes being moved
   - Check frontmatter of notes being modified
   - Verify MOC structure before planning changes to it
