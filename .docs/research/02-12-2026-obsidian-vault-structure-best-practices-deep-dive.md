---
date: 2026-02-12
status: complete
topic: "Obsidian Vault Structure Best Practices Deep Dive"
tags: [research, obsidian, vault-structure, organization, best-practices, PKM, AI-native]
git_commit: 9c4c7f4
---

# Obsidian Vault Structure Best Practices Deep Dive

## Research Question
What are the comprehensive best practices for structuring an Obsidian vault, covering folder systems, naming conventions, MOC patterns, scaling strategies, and anti-patterns — with specific attention to AI/Claude-native workflows?

## Summary
Community consensus in 2025-2026 has converged on **shallow folder hierarchies (1-3 levels max)** with **aggressive linking and MOC-based navigation**. Six major organizational systems compete: Steph Ango's minimalist approach, PARA, Zettelkasten, Johnny Decimal, Nick Milo's ACE (evolved from ACCESS), and AI-native numeric-prefix systems. The most effective vaults combine multiple methods — folders for content types, tags for broad categories, links for specific relationships, and properties for structured metadata. AI-native structures add numeric folder prefixes, CLAUDE.md files, and manifest generation for LLM discoverability. Performance holds well to 10,000+ notes but global graph view breaks first; vault structure decisions made early (flat vs deep, tags vs folders) become increasingly expensive to change at scale.

## Detailed Findings

### 1. Official Obsidian Philosophy

**Steph Ango (Obsidian CEO)** advocates a deliberately minimalist approach:

**Core Philosophy:**
- "File over app" — digital artifacts must be files you control in easy-to-retrieve formats
- "Embraces chaos and laziness to create emergent structure" — bottom-up over top-down
- "Having a consistent style collapses hundreds of future decisions into one"
- "Avoid folders for organization" — navigate via quick switcher, backlinks, internal links

**Ango's Personal Vault Structure:**
```
vault/
├── [Root]           # Personal writing (journal, essays, evergreen notes)
├── References/      # External subjects (books, movies, places, people)
├── Clippings/       # Content written by others
├── .Attachments/    # Hidden: images, audio, video, PDFs
├── .Daily/          # Hidden: YYYY-MM-DD.md daily notes
└── .Templates/      # Hidden: note templates
```

**Ango's Rules:**
- Keep one vault (avoid splitting)
- Avoid non-standard markdown
- Always pluralize categories and tags
- Use internal links profusely; include unresolved links as "breadcrumbs for future connections"
- Short property names (e.g., "start" not "start-date")
- Default to list-type properties if there's any chance of multiple values
- Use `YYYY-MM-DD` date formatting consistently
- Apply a 7-point rating scale

**GitHub Template:** [kepano/kepano-obsidian](https://github.com/kepano/kepano-obsidian) (v2.2.0, October 2025, 1.9k stars)

**Sources:** [stephango.com/vault](https://stephango.com/vault), [GitHub - kepano-obsidian](https://github.com/kepano/kepano-obsidian), [rishikeshs.com/file-over-app](https://rishikeshs.com/file-over-app/)

---

### 2. Major Organizational Systems Compared

#### PARA Method (Tiago Forte)
```
vault/
├── Projects/    # Time-bound goals with deadlines
├── Areas/       # Ongoing responsibilities
├── Resources/   # Reference materials
└── Archive/     # Completed/inactive items
```
**Question answered:** "Where does this belong right now?"
**Strength:** Great for temporary focus and current-state grouping
**Weakness:** Doesn't provide permanent addresses; Projects vs Areas distinction confusing for some
**Tip:** Tiago Forte recommends starting with only Projects and Archive — empty folders disturb flow

**Sources:** [Obsidian Forum PARA+Zettelkasten template](https://forum.obsidian.md/t/para-zettelkasten-vault-template-powerful-organization-task-tracking-and-focus-tools-all-in-one/91380)

#### Zettelkasten
```
vault/
├── 1 - Rough Notes/       # Unstructured capture
├── 2 - Source Material/   # External PDFs, papers
├── 3 - Tags/              # Category hub notes
├── 4 - Indexes/           # Maps of Content
├── 5 - Templates/         # Reusable structures
└── 6 - Atomic Notes/      # Core knowledge repository
```
**Question answered:** "What is the atomic idea here?"
**Strength:** Pure Luhmann replication starts with NO folders — a flat structure is recommended as starting point
**Weakness:** Over-customization is the common pitfall; focus on simplicity
**Naming:** YYYYMMDDHHmm Zettelkasten IDs enable date-based search ("file: 202110" finds all October 2021 notes)

**Sources:** [GitHub - benjaminkost/obsidian_template_en](https://github.com/benjaminkost/obsidian_template_en), [Obsidian Forum Zettelkasten discussion](https://forum.obsidian.md/t/provide-structure-how-do-you-use-zettelkasten-in-obsidian/35008)

#### Johnny Decimal
```
vault/
├── 00-09 Home/
│   ├── 00-00 About Me/
│   ├── 00-01 Health/
│   ├── 00-02 Legal/
│   └── ...
├── 10-19 Learning & Teaching/
├── 20-29 Work & Career/
├── 30-39 Projects & Hobbies/
├── 40-49 Content & Creativity/
├── 50-59 Knowledge Library/
├── 60-69 Archive/
└── 70-99 Reserved/
```
**Question answered:** "Where will this live forever?"
**Strength:** 100 permanent addresses — eliminates guesswork, auto-arrangement by number, muscle memory develops
**Weakness:** Rigid category limits (10 areas × 10 categories); harder to add new top-level concepts
**Key quote:** "Johnny Decimal gives every note a permanent, unchanging address that works for years"

**Sources:** [blog.shuvangkardas.com/johnny-decimal](https://blog.shuvangkardas.com/johnny-decimal-obsidian-organization-method/), [Johnny Decimal Forum template](https://forum.johnnydecimal.com/t/made-a-template-to-help-with-using-johnny-decimal-within-an-obsidian-vault/1679)

#### ACE System (Nick Milo, evolved from ACCESS)
```
vault/
├── Atlas/       # SPACE dimension — knowledge maps, MOCs
├── Calendar/    # TIME dimension — temporal organization
└── Efforts/     # IMPORTANCE dimension — active projects
```
**Evolution:** ACCESS (Atlas, Calendar, Cards, Extras, Sources, Spaces) → ACE (simplified to 3 folders)
**Migration:** "Throw Cards, Extras, and Sources into Atlas; Turn Spaces into Efforts; Now you'll have ACE"
**Strength:** "Especially suitable for creative types and free spirits who need structure but don't want to be bogged down"
**Theory:** Based on STIR model (Space, Time, Importance, Relatedness) where links provide relatedness

**Sources:** [Obsidian Forum ACE discussion](https://forum.obsidian.md/t/the-ultimate-folder-system-a-quixotic-journey-to-ace/63483), [Linking Your Thinking](https://www.linkingyourthinking.com)

#### AI-Native Numeric-Prefix (Chase Adams)
```
vault/
├── 000 Operating System/    # Templates, CLAUDE.md, automation
├── 100 Periodics/           # Daily, weekly, monthly, quarterly
├── 200 Writing & Logs/      # Drafts, AI session logs
├── 300 Entities/            # People, teams, goals, projects
├── 400 Resources/           # Books, podcasts, courses
└── 999 Triage/              # Unclassified notes
```
**Innovation:** Numeric prefixes enforce workflow order from capture → action → knowledge creation
**AI integration:** CLAUDE.md at vault root, `/commands/` directory for reusable Claude skills, tag taxonomy for AI queries
**Metadata strategy:** `#insight/pattern`, `#people/feedback-given`, `#ai/prompt` — hierarchical tags enabling AI-powered pattern surfacing

**Sources:** [curiouslychase.com/ai-native-vault-setup](https://www.curiouslychase.com/posts/ai-native-obsidian-vault-setup-guide), [gist.github.com/naushadzaman](https://gist.github.com/naushadzaman/164e85ec3557dc70392249e548b423e9)

#### FINVA Minimalist (Tim Miller)
```
vault/
├── Fleeting/     # Quick notes (mandatory weekly refactoring)
├── In Progress/  # Projects requiring >5 minutes
├── Notes/        # Permanent, finished notes
├── Views/        # MOCs and Bases for navigation
└── Archives/     # Completed projects
```
**Key principle:** "Naming notes appropriately is the most important thing" — titles contain the main idea
**Strength:** Workflow-oriented (captures → WIP → permanent → organized → archived)

**Sources:** [obsidian.rocks/how-i-use-folders](https://obsidian.rocks/how-i-use-folders-in-obsidian/)

#### PARA+Zettelkasten Hybrid (Hub-and-Spoke)
```
vault/
├── 00 Inbox/           # Capture
├── 01 Projects/        # PARA Hub
├── 02 Areas/           # PARA Hub
├── 03 Resources/       # Literature notes (PARA Hub)
├── 04 Archive/         # PARA Hub
├── 10 Zettelkasten/    # Permanent notes (Spoke of Insight)
└── 99 Attachments/     # System
```
**Integration logic:** "Physical separation + functional connection. PARA folders constitute the Hub of Action, and the Zettelkasten constitutes the Spoke of Insight."
**Workflow:** Capture → Literature notes (03) → Synthesize atomic notes (10) → Link from projects (01-02)
**Prevents:** Knowledge silos when projects archive while maintaining growing knowledge network

**Sources:** [digital-garden.ontheagilepath.net/para-and-zettelkasten-combined](https://digital-garden.ontheagilepath.net/para-and-zettelkasten-combined), [GitHub - DuskWasHere/dusk-obsidian-vault](https://github.com/DuskWasHere/dusk-obsidian-vault)

---

### 3. File Naming Conventions

**Zettelkasten IDs:** `YYYYMMDDHHmm` (e.g., `202005191856`) — enables date-based searching, chronological sorting outside Obsidian
**Kebab-case slugs:** `my-note-title.md` — growing adoption for web publishing workflows (Astro Suite, Bellboy plugins auto-convert)
**GitHub-style:** Lowercase letters, numbers, dash/period/underscore only — Vault File Renamer plugin enforces automatically
**Title case:** Human-readable titles as filenames — Steph Ango and most community members prefer this
**Priority markers:** `!!` prefix for globally critical notes, `!` for category priority (Sebastian Witowski approach)

**Consensus:** Title-as-filename is dominant. Use slugs only if publishing to web. Zettelkasten IDs are niche but powerful for temporal queries.

**Sources:** [jamierubin.net/naming-notes](https://jamierubin.net/2021/11/09/practically-paperless-with-obsidian-episode-6-tips-for-naming-notes/), [GitHub - vault-file-renamer](https://github.com/louanfontenele/obsidian-vault-file-renamer), [micheleong.com/slugify-headings](https://micheleong.com/blog/slugify-headings-for-filenames-in-obsidian)

---

### 4. Maps of Content (MOC) Best Practices

**When to create:** At Nick Milo's "mental squeeze point" — when managing multiple notes feels overwhelming. Not before.
**Size limit:** Keep under 25 items for intuitive navigation
**Conceptual consistency:** All links at same level (e.g., "Math", "Science", "English" — don't mix subjects with specific topics)
**Maintenance:** "Fleeting MOC" for unorganized notes — backlinks pane shows unprocessed content
**Auto-generation:** Dataview queries can auto-maintain MOCs: `LIST FROM [[MOC Name]] AND #tag SORT file.name asc`
**Advantages over folders:** Notes appear in multiple maps simultaneously; non-binary organization; self-documenting
**Advantages over tags:** Self-documenting (no "institutional knowledge" required); visual navigation

**Anti-patterns:**
- Don't create MOCs upfront — wait for the squeeze point
- Don't treat MOCs as permanent fixtures requiring institutional knowledge
- MOCs complement (not replace) tags and folders

**Sources:** [obsidian.rocks/maps-of-content](https://obsidian.rocks/maps-of-content-effortless-organization-for-notes/), [readwithai.substack.com/automated-mocs](https://readwithai.substack.com/p/automated-maps-of-content-in-obsidian), [blog.shuvangkardas.com/obsidian-moc](https://blog.shuvangkardas.com/obsidian-moc-map-of-content/)

---

### 5. Tags vs Folders vs Links vs Properties — The Settled Consensus

**Use all four together.** Each serves a different organizational dimension:

| Method | Best For | Dimension |
|--------|----------|-----------|
| **Folders** | Content types (journal, project, reference) | Physical location (one per note) |
| **Tags** | Broad categories, status tracking (`#status/active`) | Thematic (many per note) |
| **Links** | Specific relationships, navigation, entity connections | Relational (bidirectional) |
| **Properties** | Structured metadata (dates, URLs, ratings, authors) | Queryable data |

**Tag best practices:**
- Always lowercase
- Use singular forms (`#book` not `#books`)
- Tag consistently — same tag every time
- Leverage autocomplete to prevent typos
- Max 5 tags per note to avoid clutter
- Nested tags for hierarchies: `#status/active`, `#ai/prompt`
- Use Tag Wrangler plugin to rename/merge/reorganize at scale

**Properties increasingly replace tags** for structured metadata, offering better queryability via Dataview. Tags remain superior for quick hierarchical categorization.

**Key quote:** "Tags, links, and folders are like clothes — everyone's preference for what they use is different."

**Sources:** [Obsidian Forum definitive guide](https://forum.obsidian.md/t/folders-vs-linking-vs-tags-the-definitive-guide-extremely-short-read-this/78468), [Obsidian Forum opinionated reflection](https://forum.obsidian.md/t/an-opinionated-reflection-on-using-folders-links-tags-and-properties/78548), [practicalpkm.com/tags-effectively](https://practicalpkm.com/how-to-use-tags-effectively/), [planettash.com/tags-vs-links](https://planettash.com/2025/05/28/obsidian-tags-vs-links-which-should-you-use/)

---

### 6. Frontmatter / Properties Best Practices

**Core principles:**
- Articulate use cases first — define what questions you want properties to answer
- Avoid metadata creep: "When I started I included 'creation date' that I realized I wasn't doing anything with, so I removed them all"
- Different note types require different metadata
- Short property names for faster typing
- Default to list type if there's any chance of multiple values
- Structure must be at very top of note in YAML block between `---` lines

**Common standard fields:**
```yaml
---
type: [journal|person|project|moc|resource|book]
date: YYYY-MM-DD
tags:
  - topic
  - status/active
aliases:
  - alternate name
---
```

**Extended by note type:**
- Books: `author`, `rating` (1-7), `source`, `isbn`
- People: `role`, `org`, `last-contact`
- Projects: `status`, `area`, `deadline`

**Dataview integration:** Use consistent structures across notes in the same category to enable reliable querying. Aliases as query filters enable more precise filtering than tags alone.

**Sources:** [Obsidian Forum properties best practices](https://forum.obsidian.md/t/obsidian-properties-best-practices-and-why/63891), [ithy.com/frontmatter-obsidian](https://ithy.com/article/frontmatter-in-obsidian-qxhwc37n), [bbbburns.com/nested-yaml](https://bbbburns.com/blog/2025/07/nested-yaml-frontmatter-for-obsidian-book-notes/)

---

### 7. Scaling: What Works and What Breaks

**Performance thresholds:**
- **< 1,000 notes:** Everything works. Don't over-organize.
- **1,000-10,000 notes:** Obsidian handles well on modern hardware. Core functionality reliable.
- **10,000+ notes:** Global graph view breaks first (render times slow, force simulation unstable). Local graph still works.
- **30,000+ notes:** Search times slow noticeably.
- **50,000+ notes on mobile:** Unpractical load times.
- **100,000+ notes:** "The global graph view doesn't work at scale, but the rest seems to work even at 100k notes."
- **Individual files > 14MB:** Editing causes freezing.

**What breaks first (in order):**
1. Global graph view
2. File explorer widgets (listing thousands of files in one directory)
3. Wikilink autocomplete (`[[` takes 4 seconds per keystroke in large vaults)
4. Search performance

**Scaling strategies:**
- Distribute files across subdirectories (never thousands in root)
- Use local graph instead of global graph
- Apply filters to reduce visible node count
- Consider multi-vault approach for massive collections
- Minimize plugins until core workflow established
- MOC-based navigation instead of file explorer

**Dataview at scale:** In-memory cache of all metadata scales to "hundreds of thousands of annotated notes without issue." Use positive includes (`FROM "folder"`) not negative excludes. DataviewJS may be faster for complex queries as it skips parsing.

**Sources:** [Obsidian Forum max notes](https://forum.obsidian.md/t/maximum-number-of-notes-in-vault/1509), [Obsidian Forum terabyte vaults](https://forum.obsidian.md/t/terabyte-size-million-notes-vaults-how-scalable-is-obsidian/66674), [GitHub Dataview performance discussion](https://github.com/blacksmithgu/obsidian-dataview/discussions/2116)

---

### 8. Home Note / Dashboard Patterns

**Five approaches identified:**

1. **Simple list:** Basic linked references — `[[Inbox]]`, `[[Projects MOC]]`, `[[Books MOC]]`
2. **Mood-based (LYT):** Leading questions — "I want to…play with ideas" or "Develop my notes"
3. **Growing index:** Comprehensive vault coverage through hierarchical indexes with Dataview auto-collection
4. **Dashboard:** Combines lists with Dataview queries for statistics and project tracking
5. **Springboard:** Minimal with only essential entry points — "the ultimate gardener approach"

**Design principle:** Match your note-taking archetype (architect, gardener, or librarian)

**Sources:** [obsidian.rocks/home-notes](https://obsidian.rocks/home-notes-in-obsidian-with-examples/), [thesweetsetup.com/obsidian-dashboard](https://thesweetsetup.com/creating-obsidian-dashboard/)

---

### 9. Power User Lessons

**Eleanor Konik (15M+ words):**
- Uses Johnny Decimal organization in folders
- Processes vault overnight with Claude Code
- Commits after every modification for rollback capability
- Creates dedicated logging files for error documentation
- Key insight: "Background automation ensures neglected maintenance tasks actually get completed"

**Recovery Case Study (Obsidian Forum user "I-d-as"):**
- Created tangled vault by hybridizing atomic notes + folders + tags + properties + Dataview + Excalidraw simultaneously
- Recovery strategy: Create `1.0` (old mess) and `2.0` (rebuilt) directories; migrate notes gradually
- Maturity labeling: 🌱 Seedling → 🌿 Budding → 🌲 Evergreen
- Lesson: "The work you do will be helpful in the interim" — progress over perfection

**10,000+ note user wisdom:**
- Embrace messiness — stop striving for perfect system
- Tags and metadata more restructuring-friendly than folders
- Vaults under 100 notes don't need elaborate systems
- After 4 years: simplicity beats complexity

**Sources:** [eleanorkonik.com/claude-obsidian-level-up](https://www.eleanorkonik.com/p/claude-obsidian-got-a-level-up), [Obsidian Forum unscrambling vault](https://forum.obsidian.md/t/help-unscrambling-a-vault-once-thought-hopeless/81065), [Obsidian Forum huge vaults](https://forum.obsidian.md/t/for-those-with-huge-vaults-anything-you-d-do-differently-or-wish-you-d-known-before-starting/99754)

---

### 10. Anti-Patterns — What NOT To Do

**Structural anti-patterns:**
- Creating too many empty folders upfront — most sit empty, cluttering vault
- Deep nested hierarchies (4+ levels) — creates decision fatigue, wastes time
- Putting thousands of files in a single directory — breaks file explorer and autocomplete
- Splitting into multiple vaults prematurely — cross-vault linking unsupported

**Organizational anti-patterns:**
- Over-organizing before you have content — "Don't be prematurely prescriptive"
- Mixing capitalization in tags (`#Journal` vs `#journal`)
- Plural variants alongside singular (`#book` and `#books`)
- Over-tagging — "less is often more"
- Logging everything (digital hoarding) — filter with "Will this actually be valuable to my future self?"
- Installing too many plugins before understanding core features

**Process anti-patterns:**
- Choosing between folders/tags/links when you should use all three
- Designing for hypothetical future scale instead of current needs
- "Prioritise writing over organisation. The main thing is to actually start using it."

**Key quote:** "Build a structure the way you think you want it to work, vs. how it'll reveal itself with use" — let organization emerge.

**Sources:** [xda-developers.com/obsidian-mistakes](https://www.xda-developers.com/avoid-obsidian-setup-mistake-organized-notes/), [medium.com/stop-overthinking-obsidian](https://medium.com/@andremonthy/stop-overthinking-obsidian-a-beginners-guide-that-actually-works-c46ae9953ac7), [makeuseof.com/obsidian-vault-mistakes](https://www.makeuseof.com/i-wish-i-knew-these-before-creating-my-obsidian-vault/)

---

### 11. AI-Native Vault Design Principles

Structures optimized for Claude/LLM interaction share these patterns:

1. **CLAUDE.md at vault root** — loaded automatically every session, defines all conventions
2. **Numeric folder prefixes** — enforce alphabetical sort reflecting workflow order
3. **Flat frontmatter schema** — Obsidian Properties don't support nested YAML; use flat, descriptive field names
4. **Manifest generation** — auto-generated index files (via hooks) for AI discovery
5. **Entity-centric notes** — people, places, concepts as linkable notes enable backlinking automation
6. **Status tags** — `#status/to-evaluate` → `#status/evaluated` → `#status/adopted` for workflow tracking
7. **Dedicated AI folder** — `/commands/`, `/skills/`, automation scripts
8. **Git-backed safety** — commit after every AI modification; diff review all changes

**Minimal Second Brain template** (gokhanarkan, 2025) adds:
- Real-time manifest updates via Claude Code hooks when files change
- Weekly detection of stale inbox items (3+ days), out-of-sync manifests, dormant projects (30+ days)
- Design philosophy: "Capture without friction" — AI handles retrieval and synthesis through manifest index

**Sources:** [curiouslychase.com/ai-native-vault](https://www.curiouslychase.com/posts/ai-native-obsidian-vault-setup-guide), [GitHub - minimal-second-brain](https://github.com/gokhanarkan/minimal-second-brain), [kyleygao.com/claude-obsidian](https://kyleygao.com/blog/2025/using-claude-code-with-obsidian/)

---

### 12. Sync and Version Control

**Git versioning (recommended for AI workflows):**
- Create `.gitignore` before initial commit (ignore `.obsidian/*`, selectively track specific settings)
- SSH authentication preferred over HTTPS
- Obsidian Git plugin (Denis Olehov) for automated backups
- Branching for experiments: test new plugin on branch, merge if satisfactory

**Sync solution comparison:**
| Solution | Pros | Cons |
|----------|------|------|
| **Obsidian Sync** | Official, reliable | $4/month, only syncs while app open, flawed conflict resolution |
| **Syncthing** | Free, local P2P, fast | Discontinued first-party mobile client |
| **iCloud** | Easy for iOS users | Corruption on Windows, unidirectional failures, files "stuck uploading" |
| **Git** | Full version history, rollback | Not true sync; merge conflicts with concurrent edits |

**Sources:** [rob.cogit8.org/obsidian-git](https://rob.cogit8.org/posts/2025-03-25-obsidian-git-quick-setup-for-developers/), [martinroenn.com/syncthing](https://martinroenn.com/blog/2025/obsidian-plus-syncthing-equals-love/), [stephanmiller.com/sync-obsidian](https://www.stephanmiller.com/sync-obsidian-vault-across-devices/)

---

### 13. When to Split Vaults

**Default:** Start with a single vault. "Most people using Obsidian prefer using a single vault for all their notes."

**Split when:**
- Separate work/personal with different sharing requirements
- Performance issues at scale (slowdowns, freezing)
- Joint projects requiring selective sharing
- Different workflows for notes vs long-form writing

**Never split for:** Topic-based separation (use folders/tags instead) — cross-vault linking is unsupported.

**Sources:** [Obsidian Forum one vs multiple vaults](https://forum.obsidian.md/t/one-vault-vs-multiple-vaults/1445), [Obsidian Forum dividing big vault](https://forum.obsidian.md/t/dividing-my-big-vault-into-smaller-ones-made-it-better/91515)

## Source Conflicts

**Flat vs. structured:** Steph Ango advocates near-flat vaults with minimal folders. AI-native community favors numeric-prefixed categorical folders. Johnny Decimal users want permanent addresses. The compromise: shallow hierarchy (1-3 levels) with aggressive linking.

**Tags vs. properties:** Properties increasingly replace tags for structured metadata (better Dataview queryability). But tags remain superior for quick hierarchical categorization and built-in search. Use both.

**MOCs vs. Dataview:** Some advocate manual MOC curation for intentional knowledge building. Others prefer Dataview auto-generation for maintenance-free navigation. Best practice: manual MOCs for high-value topic areas, Dataview for routine lists.

**Single vs. multiple vaults:** Performance advocates split at 30k+ notes. Knowledge advocates keep single vault for cross-linking. Git-based AI workflows favor single vault for unified CLAUDE.md context. No universal answer — depends on use case.

**Organizational system choice:** PARA users say it's flexible. Johnny Decimal users say it scales better. ACE users say it's more creative. The real answer: pick one primary system and adapt it. Hybridize deliberately (e.g., PARA+Zettelkasten hub-and-spoke), not accidentally.

## Currency Assessment
- Most recent source: February 2026 (Minimal Second Brain template, Knowledge Vault gist)
- Topic velocity: Fast-moving (AI-native patterns emerging monthly)
- Confidence in currency: High for structural patterns (stable consensus), medium for AI integration (still evolving rapidly)

## Open Questions
- What is the optimal vault size threshold where semantic search (Smart Connections) outperforms keyword search (Grep/Glob)?
- How does CLAUDE.md length affect token consumption and session performance?
- What are production-tested patterns for multi-vault configurations with shared CLAUDE.md conventions?
- How do Obsidian Bases (new feature) change the folder-vs-tags-vs-properties balance?
- What is the real-world performance impact of Dataview queries at 50k+ notes with complex frontmatter?
- How should vault structure adapt when Obsidian 2.0 / future releases change core features?
