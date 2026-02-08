# Vault Design Domains Reference

Categories of vault organizational decisions and example questions for each domain. Use these as starting points — adapt to the specific vault being designed.

## Frontmatter Schema

**When:** Defining what metadata goes on notes, how it's structured, and what's required.

**Decision areas:**
- Property names and types (text, list, number, checkbox, date)
- Required vs optional fields per note type
- Property naming conventions (lowercase, kebab-case, camelCase)
- Obsidian-native types vs freeform YAML
- No nested YAML (Obsidian limitation)

**Example AskUserQuestion options:**
- "Frontmatter approach?" -> [Minimal (date, tags only)] [Moderate (date, tags, status, type)] [Rich (full schema per note type)] [You decide]
- "Property naming?" -> [lowercase (status, created)] [kebab-case (note-type, created-date)] [You decide]
- "Status tracking?" -> [Frontmatter status property] [Tag-based (#status/draft)] [No status tracking] [You decide]
- "Date properties?" -> [created only] [created + modified] [created + modified + reviewed] [You decide]

## MOC Strategy

**When:** Designing how Maps of Content organize and connect knowledge.

**Decision areas:**
- MOC architecture (hub-and-spoke, topic clusters, single master index)
- MOC creation approach (manual curation vs Dataview-generated)
- MOC linking direction (MOC links to notes, notes link to MOC, bidirectional)
- MOC coverage requirements (every note reachable from a MOC, or organic)
- MOC naming and placement

**Example AskUserQuestion options:**
- "MOC architecture?" -> [Hub-and-spoke (master MOC → topic MOCs → notes)] [Flat topic MOCs] [Dynamic Dataview MOCs] [You decide]
- "MOC linking direction?" -> [MOCs link out to notes] [Notes link up to MOCs] [Bidirectional] [You decide]
- "MOC coverage?" -> [Every note reachable from a MOC] [Organic (MOCs for main topics only)] [You decide]
- "MOC creation?" -> [Manual curation] [Dataview auto-generation] [Hybrid] [You decide]

## Orphan Prevention

**When:** Deciding how to prevent disconnected notes and maintain link integrity.

**Decision areas:**
- Linking conventions (when must a note link to something?)
- MOC coverage requirements
- Periodic review process
- Broken link handling

**Example AskUserQuestion options:**
- "New note linking?" -> [Must link to at least one MOC] [Must link to at least one other note] [No requirement] [You decide]
- "Orphan handling?" -> [Periodic review to link or archive] [Auto-detect and flag] [Accept orphans] [You decide]
- "Broken link handling?" -> [Fix immediately during implementation] [Flag for review] [You decide]

## Folder Boundaries

**When:** Deciding what folders exist, what goes in each, and how deep nesting goes.

**Decision areas:**
- Top-level folder structure
- Nesting depth limits
- Separation of concerns (by topic, by type, by status)
- Special folders (templates, attachments, daily notes)
- Archive strategy

**Example AskUserQuestion options:**
- "Top-level organization?" -> [By topic (Projects, Areas, Resources)] [By type (Notes, MOCs, Templates)] [Minimal (Attachments, Templates only)] [You decide]
- "Nesting depth?" -> [1 level only] [2-3 levels max] [As deep as needed] [You decide]
- "Attachment organization?" -> [Single Attachments folder] [Co-located with notes] [Subfolder per note] [You decide]
- "Archive approach?" -> [Archive folder] [Archive tag] [Delete old notes] [No archiving] [You decide]

## Tag Taxonomy

**When:** Designing the tagging system — structure, conventions, and usage patterns.

**Decision areas:**
- Hierarchical vs flat tags
- Property tags (frontmatter) vs inline tags
- Tag naming conventions
- Tag categories (status, topic, type, source)
- Tag density (few broad vs many specific)

**Example AskUserQuestion options:**
- "Tag structure?" -> [Hierarchical (topic/subtopic)] [Flat] [Hybrid (hierarchical for status, flat for topics)] [You decide]
- "Tag location?" -> [Frontmatter property tags only] [Inline tags only] [Both with clear rules] [You decide]
- "Tag naming?" -> [lowercase] [PascalCase] [kebab-case] [You decide]
- "Tag density?" -> [Few broad tags (5-10)] [Moderate (20-30)] [Many specific (50+)] [Start broad, refine] [You decide]

## Template Design

**When:** Deciding note types, template approach, and default content structure.

**Decision areas:**
- Number and types of note templates
- Template engine (Templater plugin vs core templates vs manual)
- Default frontmatter per note type
- Standard sections per note type
- Template trigger (hotkey, folder-based, manual selection)

**Example AskUserQuestion options:**
- "Template approach?" -> [Templater plugin (powerful)] [Core templates (simple)] [No templates (freeform)] [You decide]
- "Note types?" -> [2-3 basic (note, MOC, daily)] [4-6 moderate] [Many specialized types] [You decide]
- "Template trigger?" -> [Templater on new note] [Manual selection from template folder] [Folder-based auto-apply] [You decide]
- "Daily notes?" -> [Templated with links section] [Minimal (date only)] [No daily notes] [You decide]

## Anti-Patterns

**DON'T include in design (belongs in implementation):**
- Actual YAML syntax for frontmatter
- Specific Templater code or template file contents
- Folder creation commands
- Plugin configuration settings
- CSS snippet choices

**DON'T include in design (belongs in structure):**
- Exact folder paths
- Note file naming patterns
- Where specific notes will be placed
- Migration step ordering

**DO include in design (organizational decisions):**
- Which organizational paradigms to use
- Which metadata strategy to follow
- Which linking conventions to adopt
- Which template approach to take
- WHY each approach was chosen over alternatives
