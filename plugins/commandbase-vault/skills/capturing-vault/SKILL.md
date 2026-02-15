---
name: capturing-vault
description: "Use this skill when quickly capturing content into the vault from various sources. This includes creating fleeting notes from ideas or thoughts, capturing web content as vault notes, logging meeting notes or voice transcript summaries, processing inbox items into proper vault notes, and routing captured content to appropriate folders based on vault conventions. Activate when the user says 'capture to vault', 'quick note', 'save this to vault', 'clip this', 'process inbox', or 'log to vault'."
---

# Capturing to Vault

You are quickly capturing content into an Obsidian vault from various sources. This skill handles lightweight, single-note creation — fleeting thoughts, web clips, meeting notes, and inbox processing. For thorough `.docs/` artifact conversion with full frontmatter translation, use `/importing-vault` instead.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO CAPTURE WITHOUT READING VAULT CONVENTIONS FIRST
```

The vault CLAUDE.md defines folder structure, frontmatter schema, and routing rules. Without reading it, captured notes land in wrong folders with wrong frontmatter.

**No exceptions:**
- Don't create notes without knowing the vault's folder structure
- Don't guess frontmatter schema — read it from CLAUDE.md
- Don't auto-route without understanding the vault's conventions
- Don't skip source attribution for web captures

## The Gate Function

```
BEFORE creating any captured note:

1. READ: Vault CLAUDE.md for vault path, folder structure, frontmatter schema, tag taxonomy
2. DETERMINE: Capture mode (fleeting/web/meeting/inbox processing)
3. ROUTE: Determine destination using ./reference/capture-routing-rules.md
4. FORMAT: Build note content using ./reference/ofm-note-formats.md templates
5. WRITE: Create the note at the routed destination
6. VERIFY: Confirm note exists and frontmatter is valid

Skip convention reading = wrong folder + wrong frontmatter = cleanup later
```

## Scope Boundary

This skill handles quick, lightweight, single-note creation from external content.
For `.docs/` artifact conversion with full frontmatter translation and MOC integration,
use `/importing-vault` instead.

| Aspect | /capturing-vault (this skill) | /importing-vault |
|--------|-------------------------------|-----------------|
| Source | Any external content | .docs/ artifacts only |
| Depth | Minimal frontmatter, inbox routing | Full frontmatter translation, MOC integration |
| Speed | Quick, lightweight | Thorough, convention-aware |
| Review | Routes to inbox/triage folder | User reviews before placement |

## Modes

### Mode A: Fleeting Note

Use this mode for quick idea capture — thoughts, observations, questions.

**Steps:**
1. Read vault CLAUDE.md for conventions
2. Ask user for the idea/thought (or take from argument)
3. Create note with minimal frontmatter (`type: fleeting`, `created`, `status: inbox`)
4. Route to inbox/triage folder
5. Confirm creation

**Key behavior:** Speed over thoroughness. Get the idea down. Refinement happens later.

### Mode B: Web Capture

Use this mode to capture web content as a vault note.

**Steps:**
1. Read vault CLAUDE.md for conventions
2. Fetch the URL content using WebFetch tool
3. Extract key content (title, main text, key points)
4. Create note with source attribution frontmatter and callout
5. Route to resources/references folder
6. Suggest wikilinks to related existing notes (if obvious matches exist)

**Key behavior:** Clean markdown extraction, proper source attribution, no broken formatting.

### Mode C: Meeting/Log Capture

Use this mode for structured meeting notes or log entries.

**Steps:**
1. Read vault CLAUDE.md for conventions
2. Ask for meeting details or accept from argument (attendees, topics, transcript)
3. Structure into meeting template (attendees, agenda, notes, action items)
4. Create note with meeting-specific frontmatter
5. Route to meetings/daily folder
6. Extract action items as task checkboxes

**Key behavior:** Structured format with action items surfaced prominently.

### Mode D: Inbox Processing

Use this mode to review and route existing notes from inbox/triage folder.

**Steps:**
1. Read vault CLAUDE.md for conventions
2. List notes in inbox/triage folder
3. For each note, analyze content and suggest destination:
   - Check tags, title, content for routing signals
   - See ./reference/capture-routing-rules.md for routing logic
4. Present routing suggestions to user
5. Move notes to approved destinations (update frontmatter status)
6. After moves, verify no broken links

**Key behavior:** Present suggestions, let user decide. Never auto-route without approval.

## Important Guidelines

1. **Inbox as default**: When uncertain about destination, route to inbox/triage
2. **Minimal frontmatter**: Don't over-specify — `type`, `created`, `tags`, `status` are usually enough
3. **Source attribution**: Always include source for web captures (URL, date, title)
4. **No wikilinks to non-existent notes**: Only link to notes verified to exist
5. **Conflict detection**: Check for duplicate names before writing

## Red Flags - STOP and Verify

If you notice any of these, pause:

- Creating a note without knowing the vault's folder structure
- Auto-routing inbox items without user approval
- Generating wikilinks to notes you haven't verified exist
- Skipping source attribution for web captures
- Using the wrong mode (this is quick capture, not full .docs/ import)

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Inbox is fine for everything" | Route correctly when conventions are clear. Inbox is for ambiguous cases only. |
| "Frontmatter can be added later" | Minimum frontmatter now saves cleanup later. Type + created + status. |
| "This web page is simple, no need for source callout" | Always attribute sources. Provenance matters. |
| "I'll check for duplicates after" | Check before. Duplicate notes create confusion immediately. |
| "User won't mind if I auto-route" | Present suggestions. User decides. Always. |

## The Bottom Line

**Read conventions. Capture quickly. Route correctly. Attribute sources.**

Capturing is the vault's intake funnel — get content in with enough structure to be useful later. This is non-negotiable. Every capture. Every time.
