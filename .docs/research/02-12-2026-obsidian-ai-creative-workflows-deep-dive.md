---
date: 2026-02-12
status: complete
topic: "Obsidian + AI Creative Workflows Deep Dive"
tags: [research, obsidian, claude, workflows, ai-automation, vault-management, mcp]
git_commit: 9c4c7f4
---

# Obsidian + AI Creative Workflows Deep Dive

## Research Question
What are the specific, concrete creative workflows people have built for managing Obsidian vaults with AI (especially Claude), covering daily routines, knowledge graph building, content pipelines, and vault maintenance?

## Summary
This deep dive expands on the creative workflow ideas from the prior broad research (02-11-2026). Across 80+ sources, four major workflow categories emerge: (1) **Daily/periodic automation** with slash commands, starter kits, and morning/evening routines; (2) **Knowledge graph & connection discovery** using semantic embeddings, NetworkX analysis, MOC auto-generation, and gap detection; (3) **Content pipelines** transforming voice, web clips, RSS, PDFs, meetings, and reading highlights into structured knowledge; and (4) **Vault maintenance at scale** with batch metadata normalization, tag cleanup, link rot prevention, and migration tools. The most mature implementations combine Claude Code's direct filesystem access with CLAUDE.md conventions and git safety nets.

## Detailed Findings

### 1. Daily & Periodic Note Automation

#### Teresa Torres's /today Command System
**Sources:** [ChatPRD - How I AI: Teresa Torres](https://www.chatprd.ai/how-i-ai/teresa-torres-claude-code-obsdian-task-management)

Python script scans task markdown files, pulls tasks by due date, includes overdue items, adds automated Research Digest. Natural language task creation: say "new task, send thank you to Claire, do today" and Claude parses into YAML frontmatter. Morning cron queries arXiv/Google Scholar; evening script scans PDFs; Claude generates summaries emphasizing "methodology, effect size." Instead of one massive CLAUDE.md, Torres maintains dozens of focused context files in "LLM Context" vault with separate business/personal folders.

#### Personal AI Assistant with macOS Shortcuts
**Sources:** [ArtemXTech - I Built a Personal AI Assistant for My Day in Obsidian](https://artemxtech.github.io/I-Built-a-Personal-AI-Assistant-for-My-Day-in-Obsidian)

macOS Shortcut button triggers shell command → Claude Code. Agent scans calendar via AppleScript, presents summary, prompts three voice-input questions (intention, systems focus, development). Output: structured daily note with intentions and event checklist. Interactive: mention a forgotten event in conversation → agent creates it and syncs to note.

#### Starter Kits

**obsidian-claude-pkm** ([GitHub - ballred](https://github.com/ballred/obsidian-claude-pkm)): Pre-built commands `/daily`, `/weekly`, `/push`, `/onboard`. Four custom agents: note-organizer, weekly-reviewer, goal-aligner, inbox-processor. Morning (15 min), Midday (5 min), Evening (10 min), Sunday Review (30 min), Monthly Review (1 hr).

**claude-code-obsidian-starter** ([GitHub - ArtemXTech](https://github.com/ArtemXTech/claude-code-obsidian-starter)): Skills for query, tasknotes, review, client management. `/setup-memory` builds personalized CLAUDE.md from vault contents.

**Claudesidian** ([GitHub - heyitsnoah](https://github.com/heyitsnoah/claudesidian)): `/thinking-partner`, `/inbox-processor`, `/research-assistant`, `/daily-review`, `/weekly-synthesis`, `/create-command`, `/de-ai-ify` (removes AI writing patterns). Philosophy: "AI as a thinking partner, not just a writing assistant."

#### Automated Weekly Reviews
**Sources:** [GitHub - professorwug/Automated-Obsidian-Weekly-Review](https://github.com/professorwug/Automated-Obsidian-Weekly-Review), [Obsibrain - Week In Review](https://blog.obsibrain.com/other-articles/week-in-review)

Dataview rollup aggregates tasks from daily notes into weekly note. GTD methodology. AI analysis via Templater inserts complex templates. Temporal synthesis chain: daily → weekly → monthly → annual.

---

### 2. Knowledge Graph & Connection Discovery

#### Semantic Graph with Vector Embeddings
**Sources:** [GitHub - drewburchfield/obsidian-graph-mcp](https://github.com/drewburchfield/obsidian-graph-mcp)

PostgreSQL + pgvector with 1024-dim Voyage Context-3 embeddings. Five tools: `search_notes` (<1ms), `get_similar_notes` (<300ms), `get_connection_graph` (multi-hop BFS, <2s), `get_hub_notes` (<100ms), `get_orphaned_notes` (<100ms). Hub identification finds MOC candidates (notes with 10+ semantic connections). Automatic indexing with 30s debounce. Cost: 200M free tokens (~50k notes), then ~$0.12/1M tokens.

#### Topic Clustering with BERTopic
**Sources:** [GitHub - Crispigt/Plot-Obsidian-by-Topics](https://github.com/Crispigt/Plot-Obsidian-by-Topics)

Pipeline: Qwen embedding → UMAP dimensionality reduction → HDBSCAN clustering → c-TF-IDF feature extraction → LLM topic labeling. Output: interactive HTML visualizations with DataMapPlot (clickable note points) and Plotly (convex hull cluster boundaries).

#### NetworkX Graph Analysis
**Sources:** [GitHub - mfarragower/obsidiantools](https://github.com/mfarragower/obsidiantools)

Python library: `vault = otools.Vault(path).connect().gather()`. Exposes `.isolated_notes`, `.isolated_media_files`, `get_note_metadata()` DataFrame. Full NetworkX integration for degree centrality, PageRank, community detection.

#### Graphthulhu: 37-Tool MCP Server
**Sources:** [GitHub - skridlevsky/graphthulhu](https://github.com/skridlevsky/graphthulhu)

Navigate (6), Search (4), Analyze (5), Write (10), Decision (5), Journal (2), Flashcard (3), Whiteboard (2), Health (1). Analyze tools: `graph_overview`, `find_connections`, `knowledge_gaps`, `list_orphans`, `topic_clusters`. Uses BFS for path-finding, connected component analysis for clustering.

#### InfraNodus Gap Detection
**Sources:** [GitHub - noduslabs/infranodus-obsidian-plugin](https://github.com/noduslabs/infranodus-obsidian-plugin)

Three-stage: (1) Graph visualization with betweenness centrality, (2) Gap identification finding "blind holes" between disconnected clusters, (3) AI-generated bridging questions. Analyzes both wiki-links AND extracted concepts within text. Generates research questions like "How might pragmatist approaches address deconstructive critiques?"

#### Automated MOC Generation
**Sources:** [readwithai - Automated MOCs](https://readwithai.substack.com/p/automated-maps-of-content-in-obsidian)

Templater + Dataview: tag-based MOC (`LIST FROM #topic`), backlink-based MOC (`LIST without id x WHERE file.name = this.file.name FLATTEN file.inlinks as x`). Auto-updates as notes are created/linked.

#### CI/CD Connection Discovery
**Sources:** [Corti - AI-Powered Knowledge Management](https://corti.com/building-an-ai-powered-knowledge-management-system-automating-obsidian-with-claude-code-and-ci-cd-pipelines/)

Custom commands: `/connect-notes` reviews notes modified in last 7 days, suggests wikilinks. `/update-indexes` refreshes MOCs. `/suggest-merges` finds duplicates. GitHub Actions schedule daily analysis, process vault in batches of 50 files, semantic similarity threshold 0.7.

---

### 3. Content Pipelines

#### Voice → Structured Notes
**Sources:** [GitHub - gmirabella/voice-to-obsidian-ai](https://github.com/gmirabella/voice-to-obsidian-ai), [GitHub - Mikodin/obsidian-scribe](https://github.com/Mikodin/obsidian-scribe)

**SuperWhisper pipeline:** Cmd+Shift+Space → dictate → SuperWhisper transcribes → helper script pipes to Claude Code → Claude reads CLAUDE.md routing rules → routes by keywords ("need to" → Tasks, "project" → Projects/, "update meetings" → reads macOS Calendar). **Scribe plugin:** record in Obsidian → Whisper/AssemblyAI transcribe → ChatGPT transforms into summaries, action items, Mermaid charts.

#### Web Clipping → Knowledge
**Sources:** [dsebastien - Obsidian Web Clipper](https://www.dsebastien.net/supercharge-your-knowledge-capture-workflow-with-the-obsidian-web-clipper/)

Web Clipper browser extension → AI "Interpreter" processes via OpenRouter (Claude/OpenAI) → summarize, extract key points, translate, sentiment analysis → saves as structured markdown with metadata → Claude Code then searches for related notes, generates backlinks, creates MOCs.

#### RSS → Structured Summaries
**Sources:** [XDA - RSS with Obsidian and Local LLM](https://www.xda-developers.com/made-rss-better-obsidian-summaries-local-llm/)

Matcha CLI + Ollama (local). Config YAML defines feeds, LLM endpoint, output directory. Automated via Task Scheduler/cron. Incremental updates only. Custom analyst prompts per feed. Output: chronological markdown with titles, AI summaries, reading time, links.

#### Academic Research Pipeline
**Sources:** [Medium - Academic Workflow: Zotero & Obsidian](https://medium.com/@alexandraphelan/an-updated-academic-workflow-zotero-obsidian-cffef080addd), [Medium - Thesis Writing Workflow](https://medium.com/@spektrl/my-thesis-writing-workflow-obsidian-zotero-and-claude-ai-2427737f531f)

Zotero browser connector → PDF annotations → Zotero Integration plugin creates literature notes with metadata + annotations + page links → Claude analyzes highlights → atomic notes → MOC synthesis. 40-45% time on reading/notes, rest on synthesis.

#### Meeting Notes → Action Items
**Sources:** [SystemSculpt - Meeting Notes Workflow](https://systemsculpt.com/workflows/meeting-notes-to-action-items)

5-step: Capture audio → Transcribe (Whisper) → Extract decisions and action items with owner/due date/definition of done → Generate 150-250 word Slack recap → Save with diff approval. Template includes Context, Decisions, Action Items, Open Questions, Transcript sections.

#### Kindle Highlights → Connected Knowledge
**Sources:** [Hulry - Kindle Highlights AI](https://hulry.com/kindle-highlights-ai/)

Extract My Clippings.txt → place in vault → Claude organizes by book title, creates descriptive headlines, adds topic tags, links related highlights across books. No subscription dependency.

#### YouTube → Notes
**Sources:** [Glasp - YouTube Summary](https://glasp.co/features/youtube-summary)

YouTube Video Summarizer plugin (Gemini AI) or Glasp → grab transcript → AI summarize → extract key insights with timestamps → create structured note → link to related topics.

#### n8n Fleeting Notes Sorter
**Sources:** [Obsidian Forum - Local AI Fleeting Notes Sorter](https://forum.obsidian.md/t/i-made-a-local-agentic-ai-that-sorts-my-fleeting-notes-using-n8n-and-context-engineering-overnight/102675)

n8n + Ollama (local). Watches for new notes in encounters/fleeting folder. Context engineering with defined hierarchy, 15 core maps, templates per type. Determines folder, applies template, links to maps, tags with completion status. Runs overnight on 16GB RAM. Human spot-checks placement.

#### Prompt Chain Workflows
**Sources:** [QuickAdd AI Assistant](https://quickadd.obsidian.guide/docs/AIAssistant/), [GitHub - obsidian-content-pipeline](https://github.com/peritus/obsidian-content-pipeline)

QuickAdd: stack AI Assistant calls in macros, each step consumes output variable from previous step. Content Pipeline plugin: define workflows with sequential steps, dynamic AI-based routing, reference external knowledge files, archive processed files.

---

### 4. Vault Maintenance at Scale

#### Eleanor Konik's 15M-Word Vault
**Sources:** [Eleanor Konik - Claude + Obsidian + MCP](https://www.eleanorkonik.com/p/how-claude-obsidian-mcp-solved-my)

Approach: "go through files in this folder, figure out patterns, write script to put info A into location B." Results in "10 minutes or less": renamed folders from numbered to semantic names, fixed broken links, reformatted daily notes into themed log files, created custom Publish theme, converted Dataview metadata to Bases format. Key insight: optimize for retrieval ease, strategically duplicate data.

#### Python LLM Metadata Cleanup
**Sources:** [Karan Sharma - Cleaning up Notes with LLM](https://mrkaran.dev/posts/cleanup-obsidian/)

Python script: extract existing frontmatter → LLM infers title, categories, tags, status, priority → merge (preserve existing) → write back. Example: raw note about "Setting up BTRFS on Arch" auto-receives tags "linux," "filesystem," "arch."

#### obsidian-metadata CLI
**Sources:** [GitHub - natelandau/obsidian-metadata](https://github.com/natelandau/obsidian-metadata)

`pip install obsidian-metadata`. Commands: `--dry-run` preview, `--export-csv`, `--import-csv` for batch updates, `--create-backup`. CSV format: path, type, key, value. Supports: add, rename, delete, move, transpose between frontmatter and inline.

#### py-obsidianmd Library
**Sources:** [GitHub - selimrbd/py-obsidianmd](https://github.com/selimrbd/py-obsidianmd)

Convert frontmatter to inline, organize in callouts, filter by metadata, batch modify. `notes.metadata.move(fr=MetadataType.FRONTMATTER, to=MetadataType.INLINE)`.

#### Dataview to Properties Migration
**Sources:** [QuickAdd - Migrate Dataview Properties](https://quickadd.obsidian.guide/docs/Examples/Macro_MigrateDataviewProperties)

QuickAdd macro runs `migrateDataviewToFrontmatter.js`. Converts `Reference:: [[link]]` to proper YAML frontmatter. Re-reads files after updates before removing inline syntax.

#### Link Rot Prevention
**Sources:** [Ben Congdon - Preventing Link Rot](https://benjamincongdon.me/blog/2021/09/19/Preventing-Link-Rot-in-my-Obsidian-Vault/)

wayback-archiver (Rust CLI): finds all URLs in vault → checks for recent Wayback Machine snapshots → archives missing ones → outputs JSON mapping. Runs via crontab.

#### Tag Management
**Sources:** [GitHub - pjeby/tag-wrangler](https://github.com/pjeby/tag-wrangler)

Tag Wrangler plugin: drag-and-drop rename/reorganize, batch rename hierarchical tags, merge with confirmation. AI Tagger Universe: analyzes content, suggests tags from local or cloud LLMs. Metadata Auto Classifier: AI-powered classification.

#### Vault Quality Auditing
**Sources:** [GitHub - Vinzent03/find-unlinked-files](https://github.com/Vinzent03/find-unlinked-files), [Obsidian CLI Ops](https://data-wise.github.io/obsidian-cli-ops/)

Find orphaned files/broken links plugin. Obsidian CLI Ops: `check-links`, `find-orphans`, `find-duplicates`, `analyze --stats`.

#### Flashcard Generation
**Sources:** [GitHub - ad2969/obsidian-auto-anki](https://github.com/ad2969/obsidian-auto-anki), [Spaced Repetition AI](https://obsidian-spaced-repetition-ai.vercel.app/)

Auto Anki: GPT generates flashcards → pushes to Anki via AnkiConnect. SRAI: AI generation + FSRS algorithm for scheduling. True Recall: native FSRS v6 following SuperMemo's 20 rules.

---

### 5. Cross-Cutting Patterns

#### CLAUDE.md as Vault Constitution
Every mature workflow starts with a comprehensive CLAUDE.md at vault root. Eleanor Konik's grew from simple to extensive. Teresa Torres maintains dozens of focused context files instead of one monolith. The common elements: vault structure, naming conventions, tagging taxonomy, forbidden actions, tone preferences.

#### Git as Safety Net
Universal consensus: git before AI writes. Eleanor Konik: "multiple good backups." Community standard: git init vault, commit after every AI change, diff review all modifications. The obsidian-git plugin automates commits at intervals.

#### Slash Commands as Workflow Entry Points
All starter kits converge on slash commands: `/today`, `/daily-review`, `/weekly-synthesis`, `/research`, `/brainstorm`, `/connect-notes`. These are implemented as `.claude/commands/` markdown files that Claude Code reads as instructions.

#### Approval-Based Editing
SystemSculpt and other mature workflows show diffs before writing. Claude Code's permission model (YOLO/Safe/Plan) maps naturally. The best workflows separate "suggest" from "execute."

## Source Conflicts

**Embedded plugins vs. direct filesystem**: Claudesidian and Agent Client offer rich in-Obsidian UI but aren't approved for community plugins. Direct filesystem access via Claude Code is simpler, more stable, and scales better for batch operations, but lacks semantic search and Templater integration.

**Cloud vs. local AI**: n8n + Ollama workflows run entirely locally (16GB RAM). Cloud approaches (Claude API) are more capable but incur costs and require internet. The fleeting notes sorter demonstrates that local models handle routing/classification well, while synthesis tasks benefit from Claude.

**MOC strategies**: Dataview auto-MOCs vs. AI-generated MOCs vs. human-curated MOCs. Dataview auto-updates but captures unintended connections. AI discovers non-obvious relationships but needs human validation. Best practice emerging: use Dataview for mechanical aggregation, AI for discovery, human for curation.

**Single CLAUDE.md vs. context library**: Torres uses many focused files; most others use a single growing CLAUDE.md. Trade-off: granularity vs. maintenance overhead.

## Currency Assessment
- Most recent sources: January-February 2026
- Topic velocity: Very fast-moving (new starter kits, plugins, and MCP servers appearing weekly)
- Confidence in currency: High — the MCP + Claude Code ecosystem is actively evolving
- Confidence in patterns: Medium-high — core patterns (CLAUDE.md, git safety, slash commands) are stabilizing

## Open Questions
- What's the optimal size/complexity threshold for CLAUDE.md before switching to a context library?
- How well do semantic embedding approaches (Voyage, Qwen) handle domain-specific terminology in personal vaults?
- What's the failure rate of AI-generated backlinks and MOC suggestions? (No quantitative data found)
- Can n8n + local AI workflows match Claude Code quality for complex synthesis tasks?
- What's the practical limit for batch processing vault size before workflows break down?
- How do these workflows compose? Can you chain daily automation → graph analysis → content pipeline → maintenance?
