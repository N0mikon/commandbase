---
name: brainstorming-vault
description: "Use this skill when exploring direction and preferences for an Obsidian vault before building structure. This includes discussing folder hierarchy vs flat tags, MOC strategies, linking philosophies (Zettelkasten vs PARA vs hybrid), template approaches, and plugin decisions for knowledge management."
---

# Brainstorming Vault

You are exploring direction and preferences for an Obsidian vault or knowledge management system through adaptive questioning BEFORE building any structure. This skill activates when users want to brainstorm vault organization, discuss note-taking philosophy, or settle knowledge management direction. It produces a `.docs/brainstorm/` artifact that captures vault philosophy and preferences.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
CAPTURE VAULT PHILOSOPHY BEFORE BUILDING
```

Vault brainstorming settles organizational philosophy (Zettelkasten vs PARA vs hybrid, flat vs nested, links vs folders) BEFORE creating any folder structure, templates, or MOCs. Building without philosophy leads to reorganization cycles.

**No exceptions:**
- Don't assume users want Zettelkasten — it's one philosophy among many
- Don't skip brainstorming because the vault is "simple" — even a personal journal has organizational decisions
- Don't recommend plugins before settling on philosophy — tools serve philosophy, not the reverse
- Don't reference a specific vault's current state — brainstorming captures ideal direction, not current reality

## The Gate Function

```
BEFORE generating questions:

1. IDENTIFY: What vault purpose or topic is being brainstormed?
2. ASSESS: Which vault domains are relevant? (structure, linking, templates, organization, plugins)
3. GENERATE: Create domain-specific discussion topics
4. CONFIRM: User selects which topics to brainstorm
5. ONLY THEN: Begin 4-question rhythm per topic

Skipping domain assessment = generic questions = vault that doesn't fit the user
```

## Initial Response

When invoked, determine the vault purpose:

### If vault topic provided as argument:
1. Identify which vault domains are relevant
2. Present topics for selection

### If no argument provided:
```
I'll help you explore direction and preferences for your Obsidian vault.

What's the vault's purpose? For example:
- Personal knowledge management
- Project documentation
- Research notes
- Second brain / Zettelkasten
- Specific topic (e.g., programming notes, book notes)

Describe what you want the vault to help you do.
```

### After purpose is identified:
```
Vault Purpose: [Purpose from input]
Relevant Domains: [Which of the 5 vault domains apply]

Topics to explore:

[ ] [Topic 1] - [What philosophy this settles]
[ ] [Topic 2] - [What philosophy this settles]
[ ] [Topic 3] - [What philosophy this settles]
[ ] [Topic 4] - [What philosophy this settles]

Which topics should we cover?
```

Present topics using AskUserQuestion with `multiSelect: true`. NO "skip all" option — user invoked this command to brainstorm.

## Vault Domains

See `reference/vault-question-domains.md` for domain-specific question templates.

Unlike code brainstorming (which detects domain via action verbs), vault brainstorming always draws from 5 fixed domains. The question is which are relevant, not which type the topic is.

**Vault Domains:**

| Domain | What It Settles |
|--------|----------------|
| Structure | Folder hierarchy, flat vs nested, MOC strategy, daily notes placement |
| Linking | Wikilinks vs markdown, backlink philosophy, link density, connection patterns |
| Templates | Templater vs core, note types, metadata strategy, frontmatter approach |
| Organization | PARA vs Zettelkasten vs hybrid, tag taxonomy, naming conventions |
| Plugins | Minimal vs maximal, Dataview usage, community plugins, automation level |

**Domain Selection Process:**
1. All 5 domains are potentially relevant for any vault
2. Identify which domains have the most impact for this vault's purpose
3. Present 3-4 most relevant domains as topics
4. User selects which to explore

## Process

### Step 1: Topic Selection

Present 3-4 vault-specific topics using AskUserQuestion with `multiSelect: true`.

**Topic Generation Guidelines:**
- Topics must be specific to THIS vault's purpose, not generic
- Each topic should represent a real philosophical decision
- Include mini-description of what philosophy each topic settles
- Draw from `reference/vault-question-domains.md`

### Step 2: Deep Brainstorming

For each selected topic, use the 4-question rhythm:

1. Announce: "Let's explore [Topic]"
2. Ask 4 questions using AskUserQuestion
   - 2-3 concrete options per question
   - Options reflect real vault philosophies: "Zettelkasten" not "Option A"
   - Include "You decide" option when reasonable
   - "Other" is added automatically by the tool
3. After 4 questions, check: "More questions about [topic], or move on?"
   - If "More" → ask 4 more, check again
   - If "Move on" → proceed to next topic

**Question Design:**
- Each answer can inform the next question (e.g., choosing Zettelkasten affects linking questions)
- Questions probe philosophy, NOT tool configuration ("flat or nested?" not "how many folder levels?")
- If user picks "Other", capture input, reflect back, confirm understanding

### Step 3: Scope Guardrail

If user mentions something outside the vault brainstorm scope:

```
"[Mentioned capability] sounds like it belongs in a separate brainstorm or implementation task.
I'll note it as a deferred idea so it's not lost.

Back to [current topic]: [return to current question]"
```

Track deferred ideas for inclusion in brainstorm artifact.

### Step 4: Brainstorm Artifact Creation

After all topics explored:

1. Confirm: "Ready to capture these decisions?"
2. Spawn a `docs-writer` agent via the Task tool:

   ```
   Task prompt:
     doc_type: "brainstorm"
     topic: "<vault purpose/name>"
     tags: [vault]
     content: |
       <compiled brainstorm using ./templates/brainstorm-template.md>
   ```

3. Present summary and next steps

## Output Format

```
BRAINSTORM COMPLETE
===================

Brainstorm captured at: .docs/brainstorm/{topic-name}.md

Philosophy settled:
- [Key philosophy choice 1]
- [Key philosophy choice 2]
- [Key philosophy choice 3]

Deferred ideas: [count or "None"]

Next steps:
- When Vault BRDSPI is available: /starting-vault to initialize workspace
- For now: Use these decisions to guide vault setup manually
- Reference this brainstorm when making vault structure decisions
```

## Error Recovery

**Recoverable errors** (fix and continue):
- User unclear on vault purpose: Ask clarifying question about what the vault should help them do
- Multiple vault purposes: Ask which to focus on, note others as deferred

**Blocking errors** (stop and ask):
- No vault purpose identified: Cannot proceed without knowing what the vault is for
- All topics declined: Ask if user wants different topics or to skip brainstorming

## Red Flags - STOP and Refocus

If you notice any of these, pause:

- Asking code-specific questions (API design, CLI flags, UI layout) — wrong domain
- Recommending specific plugin configurations — that's implementation, not philosophy
- Asking about existing vault structure — brainstorming captures ideal, not current state
- Generating generic questions not tailored to this vault's purpose
- Not tracking deferred ideas
- Asking more than 4 questions before checking "More or move on?"

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Everyone uses Zettelkasten" | Many philosophies exist. Ask, don't assume. |
| "This vault is simple, skip brainstorming" | Simple vaults have organizational decisions. Capture them. |
| "I should suggest best practices" | Best practices vary by philosophy. Capture philosophy first. |
| "Let me check what plugins are popular" | Plugins serve philosophy. Settle philosophy first. |
| "The user can reorganize later" | Reorganization is painful. Get direction right upfront. |

## The Bottom Line

**Brainstorming captures VAULT PHILOSOPHY, not VAULT CONFIGURATION.**

The user knows what they want to manage. Your job is to extract their organizational philosophy through concrete questions — not template syntax, not plugin settings, not folder naming rules. Philosophy first, implementation later.

This is non-negotiable. Every vault. Every time.
