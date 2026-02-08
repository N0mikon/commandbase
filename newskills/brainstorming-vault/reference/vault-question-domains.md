# Vault Question Domains Reference

This reference provides vault-specific direction question templates. Use these as starting points — adapt questions to the specific vault purpose being brainstormed. Questions should probe PHILOSOPHY, not configuration details.

## Structure Domain

**What it settles:** How the vault is physically organized — folders, hierarchy depth, where different note types live.

**Default Topics:**
1. **Hierarchy Approach** - Flat with tags or nested folder hierarchy
2. **MOC Strategy** - How Maps of Content connect knowledge
3. **Daily Notes** - Where temporal notes live and how they relate to permanent notes
4. **Note Placement** - Where new notes go by default

**Direction Questions:**

Hierarchy:
- "Flat files with tags or nested folder hierarchy?" → [Flat + tags] [Nested folders] [Shallow folders + tags] [You decide]
- "How deep should folders go?" → [One level only] [2-3 levels max] [As deep as needed] [You decide]
- "Separate folders by note type or by topic?" → [By type (fleeting/literature/permanent)] [By topic (projects/areas)] [Mix] [You decide]

MOC:
- "One master MOC or topic-specific hubs?" → [Single master index] [Topic hubs] [Both] [You decide]
- "MOCs link to notes, or notes link to MOCs?" → [MOCs link out] [Notes link up] [Both directions] [You decide]

Daily Notes:
- "Daily notes in root or dated subfolder?" → [Root] [Year/Month subfolder] [Dedicated dailies folder] [You decide]
- "Daily notes link to other notes, or standalone?" → [Active linking] [Standalone journals] [You decide]

---

## Linking Domain

**What it settles:** How notes connect to each other — link format, density, and connection philosophy.

**Default Topics:**
1. **Link Format** - Wikilinks vs standard markdown links
2. **Connection Philosophy** - How aggressively notes should be linked
3. **Link Patterns** - Hub-and-spoke vs organic web vs sequential
4. **Backlink Usage** - How backlinks inform note discovery

**Direction Questions:**

Format:
- "Wikilinks or standard markdown links?" → [Wikilinks [[note]]] [Markdown [note](note.md)] [You decide]
- "Display link titles or raw filenames?" → [Titles (aliases)] [Filenames] [You decide]

Philosophy:
- "Link aggressively or curate connections?" → [Link everything related] [Only meaningful connections] [You decide]
- "Link at creation or during review?" → [Link immediately] [Link during review sessions] [Both] [You decide]

Patterns:
- "Hub-and-spoke or organic web?" → [Hub-and-spoke (MOC-centered)] [Organic web (emergent)] [Mix] [You decide]
- "Sequential linking (note chains) or associative?" → [Sequential chains] [Associative clusters] [Both] [You decide]

---

## Templates Domain

**What it settles:** How notes are structured by default — templates, frontmatter, and note types.

**Default Topics:**
1. **Template Approach** - Templater plugin vs core templates vs manual
2. **Note Types** - How many distinct note types and what defines them
3. **Frontmatter Strategy** - What metadata goes on notes and how structured
4. **Automation Level** - How much happens automatically on note creation

**Direction Questions:**

Templates:
- "Templater plugin or core templates?" → [Templater (powerful)] [Core templates (simple)] [Manual (no templates)] [You decide]
- "Strict note types or freeform?" → [Strict (always use a template)] [Freeform (template optional)] [You decide]

Note Types:
- "How many distinct note types?" → [2-3 (simple)] [4-6 (moderate)] [Many specialized types] [You decide]
- "Fleeting/literature/permanent distinction?" → [Yes, strict separation] [Soft distinction] [No, all notes equal] [You decide]

Frontmatter:
- "Frontmatter on every note or only structured notes?" → [Every note] [Only structured] [You decide]
- "Minimal frontmatter or rich metadata?" → [Minimal (date, tags)] [Rich (date, tags, status, type, source)] [You decide]

---

## Organization Domain

**What it settles:** The overarching organizational philosophy — how knowledge is categorized, tagged, and named.

**Default Topics:**
1. **Philosophy** - PARA, Zettelkasten, hybrid, or custom approach
2. **Tag Strategy** - How tags are structured and used
3. **Naming Conventions** - How notes are titled and identified
4. **Lifecycle Management** - How notes mature and are archived

**Direction Questions:**

Philosophy:
- "PARA, Zettelkasten, or hybrid?" → [PARA (Projects/Areas/Resources/Archive)] [Zettelkasten (atomic, linked)] [Hybrid] [You decide]
- "Knowledge-centric or project-centric?" → [Knowledge (ideas evolve)] [Projects (tasks complete)] [Both coexist] [You decide]

Tags:
- "Flat tags or hierarchical (nested)?" → [Flat] [Hierarchical (topic/subtopic)] [You decide]
- "Tags for status, for topic, or both?" → [Status only] [Topic only] [Both] [You decide]
- "Few broad tags or many specific tags?" → [Few broad] [Many specific] [Start broad, refine] [You decide]

Naming:
- "Descriptive titles or ID-based?" → [Descriptive (full sentence)] [ID-prefixed (202602071200)] [You decide]
- "Title case or lowercase?" → [Title Case] [lowercase] [You decide]

---

## Plugins Domain

**What it settles:** The role of community plugins and automation in the vault workflow.

**Default Topics:**
1. **Plugin Philosophy** - Minimal core-only vs maximal community-driven
2. **Dataview Usage** - Whether and how much to rely on dynamic queries
3. **Automation Level** - What happens automatically vs manually
4. **Portability Concerns** - How much plugin lock-in is acceptable

**Direction Questions:**

Philosophy:
- "Minimal (core only) or maximal (community plugins)?" → [Minimal] [Moderate (5-10 plugins)] [Maximal (whatever helps)] [You decide]
- "Prioritize portability or power?" → [Portability (works without plugins)] [Power (best tool for each job)] [You decide]

Dataview:
- "Use Dataview for dynamic queries?" → [Yes, extensively] [Sparingly] [No, static only] [You decide]
- "Inline metadata or frontmatter-only for queries?" → [Inline (field:: value)] [Frontmatter only] [You decide]

Automation:
- "Auto-move notes to folders based on tags/type?" → [Yes, automated] [No, manual placement] [You decide]
- "Auto-generate daily notes?" → [Yes, on startup] [Manual creation] [You decide]

---

## Anti-Patterns

**DON'T ask (belongs in implementation):**
- Specific plugin configuration questions
- Template syntax or YAML field names
- Folder path naming (e.g., "call it 01-Projects or Projects?")
- CSS snippet or theme choices

**DON'T ask (belongs in code brainstorming):**
- API design, CLI interface, or UI layout questions
- Programming architecture decisions

**DO ask (philosophy questions):**
- Which organizational paradigm? (PARA vs Zettelkasten vs custom)
- Which linking philosophy? (aggressive vs curated, hub vs web)
- Which metadata approach? (minimal vs rich, strict vs freeform)
- Which automation philosophy? (manual control vs automated workflows)
