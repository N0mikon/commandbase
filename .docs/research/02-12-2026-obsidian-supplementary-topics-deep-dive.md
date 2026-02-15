---
date: 2026-02-12
status: complete
topic: "Obsidian Supplementary Topics Deep Dive: Local AI, Storage Models, Multi-Vault, and Mobile Access"
tags: [research, obsidian, local-llm, privacy, spaced-repetition, multi-vault, mobile, ai-workflows]
git_commit: n/a
---

# Obsidian Supplementary Topics Deep Dive

## Research Question
What are the current options and best practices for four cross-cutting concerns in AI-managed Obsidian vaults: local/private AI models, spaced repetition storage architectures, multi-vault configurations, and mobile AI access?

## Summary
Four topics fell outside the main research sections but remain relevant for vault management decisions. **Local AI** is viable via Ollama/LM Studio with plugins like Private AI, Local GPT, and Smart Second Brain — privacy is preserved but capability lags behind cloud Claude significantly. **Spaced repetition storage** presents a clear trade-off: SQLite (True Recall, Anki-style) keeps notes clean but locks data in a database; in-note embedding (SRAI, Spaced Repetition Recall) preserves portability but clutters markdown. **Multi-vault configurations** work via separate MCP server instances on different ports, with CLAUDE.md patterns shareable through symlinks, `.claude/rules/` directories, or the `claude-sync` npm package. **Mobile AI access** remains severely limited — most AI plugins are desktop-only, MCP doesn't work on mobile, and the best workarounds are SSH tunneling to desktop Claude Code (via Happy Coder or Termius) or voice-to-vault apps.

## Detailed Findings

### 1. Cloud vs. Local AI for Obsidian Vaults

#### The Privacy Tension
Cloud AI (Claude, GPT-4) sends vault content to external servers for processing. For personal journals, work notes, and sensitive knowledge bases, this creates legitimate privacy concerns. As one source notes: "Most AI plugins connect to outside AI services, requiring an API key, which means parts of your notes are sent over the internet to be processed."

Obsidian's local-first philosophy aligns naturally with local AI — the vault stays on disk, and the AI should too.

#### Local AI Plugin Landscape

**Private AI** — Simplest privacy-first option:
- Connects to locally running LM Studio server (127.0.0.1:1234)
- Auto-searches relevant notes, cites sources in responses
- Free, lightweight, cross-platform (Mac/Windows)
- "Your notes never leave the device and use local processing only"

**Local GPT** (pfrankov) — Most versatile local option:
- Works with Ollama for complete offline operation
- RAG support: uses context from links, backlinks, and PDFs
- Vision-capable with compatible models
- Community-contributed actions (summarize, grammar, extract action items)
- Requires separate "AI Providers" plugin for backend configuration

**Smart Second Brain** — Best RAG implementation:
- Full offline via Ollama with Orama vector store
- Hierarchical tree summarization for retrieval
- Chat session save/resume
- Recommended embedding model: mxbai-embed-large
- Caveat: Obsidian Sync users must exclude vectorstore folder

**Local LLM Helper** — Lightweight alternative:
- Works with any OpenAI-compatible server (Ollama, LM Studio, vLLM)
- Persona selection, streaming output, chat history (3 turns)
- Status bar integration

**Time Garden** — Journaling-focused:
- Local AI insights for pattern discovery in journals
- $99 "Eternal" tier adds AI features (summaries, ratings, Q&A)
- Closed-source plugin component despite "local AI" marketing
- Privacy documentation lacks technical detail

#### Local AI Backend Options

| Backend | Setup | Performance | Models |
|---------|-------|-------------|--------|
| **Ollama** | `brew install ollama` / Windows installer | "Pretty zippy" on M1+ | Llama 3.1, Mistral, Gemma, Dolphin |
| **LM Studio** | GUI download, model browser | Good on modern hardware | Wide model library, GGUF format |
| **GPT4All** | GUI download, LocalDocs feature | Variable | Llama 3, Mistral, custom fine-tunes |

#### The Capability Gap
Local models (7B-70B parameters) cannot match Claude Opus/Sonnet for complex vault operations — restructuring, multi-file refactoring, nuanced writing. They work well for: summarization, tag suggestion, simple Q&A over notes, and flashcard generation. For commandbase-vault skills that require sophisticated reasoning, cloud Claude remains necessary.

**Sources:** [MakeUseOf - Obsidian Local LLM](https://www.makeuseof.com/obsidian-local-llm-integration/), [Annvix - Using Obsidian with Local LLM](https://annvix.com/blog/using-obsidian-with-a-local-llm), [TFTHacker - AI and Vault Privacy](https://tfthacker.com/article-ai-obsidian-protect-privacy), [GitHub - pfrankov/obsidian-local-gpt](https://github.com/pfrankov/obsidian-local-gpt), [GitHub - Smart Second Brain](https://github.com/your-papa/obsidian-Smart2Brain)

### 2. Centralized vs. In-Note Storage for Spaced Repetition

#### The Core Trade-off
Spaced repetition plugins must store scheduling metadata (next review date, difficulty, interval) somewhere. Two architectures compete:

**Centralized (SQLite/Database):** True Recall, Aosr, Anki export plugins
- Card data stored in `.true-recall/true-recall.db` or external Anki database
- Notes remain pure markdown — no scheduling clutter
- Developer rationale: "Instead of forcing you to write cards inside your text files, I decided to use SQLite"
- Easier cross-device sync via database replication
- Risk: data locked in proprietary format, migration complexity

**Embedded (In-Note):** SRAI, Spaced Repetition Recall, Better Recall
- Scheduling data stored alongside note content in markdown files or sidecar JSON
- Cards travel with notes — full portability
- No external dependencies
- Risk: clutters note content, may conflict with other plugins

**Hybrid (Sidecar JSON):** Spaced Repetition Recall offers both modes
- Separate `tracked_files.json` keeps scheduling data out of notes
- Algorithm switching (Default, Anki SM-2, FSRS) only works in JSON mode
- Clean compromise but requires coordination between files

#### FSRS vs. SM-2 Algorithm
All modern plugins are converging on FSRS (Free Spaced Repetition Scheduler):
- Trained on 700M reviews from 20,000 users (vs. SM-2's limited 1987 data)
- 20% reduction in reviews while maintaining retention
- Tracks memory stability, retrieval strength, and spacing effect
- Available in Anki 23.10+, True Recall, SRAI, Better Recall, Spaced Repetition Recall

#### Plugin Comparison

| Plugin | Storage | Algorithm | AI Generation | Price |
|--------|---------|-----------|---------------|-------|
| **True Recall** | SQLite | FSRS v6 | Yes (7 models via OpenRouter) | $120/year |
| **SRAI** | In-note (`SR/` folder) | FSRS | Yes (OpenAI) | Free |
| **Spaced Repetition Recall** | In-note or JSON | SM-2, Anki, FSRS | No | Free |
| **Better Recall** | In-vault | SM-2, FSRS | No | Free |
| **Aosr** | SQLite (`aosr.db`) | Custom | No | Free |

#### Recommendation for commandbase-vault
For vault skills that interact with spaced repetition, prefer the sidecar JSON approach (Spaced Repetition Recall) — it keeps notes clean while remaining filesystem-accessible for Claude Code operations. SQLite databases require specialized tooling that doesn't integrate with Read/Write/Edit tools.

**Sources:** [GitHub - True Recall](https://github.com/pieralukasz/true-recall), [GitHub - SRAI](https://github.com/ai-learning-tools/obsidian-spaced-repetition-ai), [ObsidianStats - Spaced Repetition Comparison](https://www.obsidianstats.com/posts/2025-05-01-spaced-repetition-plugins), [Obsidian Forum - True Recall](https://forum.obsidian.md/t/i-built-a-native-fsrs-algorithm-for-obsidian-with-ai-flashcard-generation/109962)

### 3. Multi-Vault Configurations with AI

#### Vault Separation Strategies

**Complete separation** (most secure):
- Separate vaults for work and personal content
- Prevents accidental information leakage
- Obsidian Sync supports up to 5 remote vaults at same price
- Benefits: faster startup, eliminates cross-contamination

**Sub-vault approach** (partial isolation):
- Work computers access only a work subfolder
- Personal computers see everything
- Files in sub-vault visible from main vault for linking
- Visibility doesn't work in reverse

**Folder separation** (simplest):
- Single vault with work/personal folders
- Can exclude private folders from search
- Less secure but easier to maintain

#### MCP Server Configuration for Multiple Vaults

Each vault needs its own MCP server instance on a unique port:

```json
{
  "mcpServers": {
    "obsidian-personal": {
      "command": "npx",
      "args": ["obsidian-mcp", "/path/to/PersonalVault"]
    },
    "obsidian-work": {
      "command": "npx",
      "args": ["obsidian-mcp", "/path/to/WorkVault"]
    }
  }
}
```

Some servers support vault ID systems with per-vault API keys and ports:
```json
[
  { "id": "personal", "port": 27124, "vaultPath": "/path/to/Personal" },
  { "id": "work", "port": 27125, "vaultPath": "/path/to/Work" }
]
```

**Critical:** Each vault's Local REST API plugin must listen on a unique port. Port conflicts cause authorization errors.

#### Sharing CLAUDE.md Patterns Across Vaults

Three methods for keeping AI configuration in sync:

**Symlinks** (most reliable):
```bash
ln -sf /path/to/shared/CLAUDE.md /path/to/vault/CLAUDE.md
```
Claude Code follows symlinks transparently — edits modify the target file.

**`.claude/rules/` directory** (most flexible):
Shared rules in a common directory, vault-specific rules alongside:
```
.claude/
├── CLAUDE.md          # Vault-specific
└── rules/
    ├── shared/        # Symlinked from central repo
    └── vault-specific.md
```

**claude-sync npm package** (automated):
Git-aware CLI that tracks Claude config files across projects via symlinks in a centralized sync repository. Commands: `sync_init`, `sync_push`, `sync_pull`, `sync_status`.

#### For commandbase-vault Skills
Direct filesystem approach handles multi-vault naturally — `cd` into whichever vault you want to work with. Each vault has its own CLAUDE.md. Shared conventions live in `~/.claude/CLAUDE.md` (global) or symlinked `.claude/rules/`. No special configuration needed.

**Sources:** [GitHub - cyanheads/obsidian-mcp-server](https://github.com/cyanheads/obsidian-mcp-server), [Obsidian Forum - Split Vault Strategies](https://forum.obsidian.md/t/better-strategies-to-split-vault-in-work-and-privat/103696), [Claude Code Rules Directory](https://claudefa.st/blog/guide/mechanics/rules-directory), [claude-code-config-sync npm](https://www.npmjs.com/package/claude-code-config-sync)

### 4. Mobile Vault Access with AI

#### Current State: Severely Limited
Most AI plugins are desktop-only. MCP servers do not work on mobile (Claude Mobile doesn't support MCP protocol). The mobile Obsidian sandbox prevents CLI tool execution.

**Desktop-only AI plugins (confirmed):**
- Obsidian Copilot — "Mobile support is in the roadmap" (no timeline, since Nov 2023)
- Smart Composer — Desktop-oriented architecture
- Claudian — "Desktop only (macOS, Linux, Windows)" — requires Claude Code CLI
- Most MCP-dependent integrations

#### Workarounds That Work

**SSH to Desktop Claude Code** (best option):
- SSH server on desktop + Tailscale VPN + Termius mobile app
- Run full Claude Code sessions remotely via terminal
- Desktop must remain running; terminal-only interface
- One blogger: "Claude Code is better on your phone" via SSH

**Happy Coder** (purpose-built mobile client):
- Free, open-source native apps for iOS, Android, Web
- End-to-end encryption (TweetNaCl, same as Signal)
- Control multiple Claude Code instances in parallel
- Push notifications for permission requests and task completion
- Still requires desktop running Claude Code — mobile is interface only

**Voice-to-vault apps:**
- Obsidian Voice: web-based transcription → organized vault notes
- Voice Inbox (iOS only, iOS 17+): transcription with high accuracy
- AI Assistant plugin: speech-to-text at cursor position

**Quick capture automation:**
- Android: Tasker + Termux + Git SSH for automated sync
- iOS: Shortcuts for URL-based task creation
- Focus: capture only, not AI-powered workflows

#### What Doesn't Work on Mobile
- MCP servers (no mobile MCP support)
- Any plugin requiring CLI tools
- Direct Claude Code execution
- Local LLM inference (hardware limitations)

#### Outlook
Mobile AI integration depends on either: (1) Claude Mobile adding MCP protocol support, (2) plugin developers investing in mobile-compatible architectures, or (3) remote access solutions like Happy Coder maturing. For now, mobile remains a capture-and-sync endpoint, not an AI workflow platform.

**Sources:** [3 Ways to Use Claude Code on Mobile](https://apidog.com/blog/claude-code-mobile/), [Happy Coder](https://happy.engineering/), [Claude Code Better on Phone](https://harper.blog/2026/01/05/claude-code-is-better-on-your-phone/), [Obsidian Copilot Mobile Discussion](https://github.com/logancyang/obsidian-copilot/discussions/165), [Mobile Development Docs](https://docs.obsidian.md/Plugins/Getting+started/Mobile+development)

## Source Conflicts

**Cloud vs. local capability:** Local AI advocates emphasize privacy preservation, but no source claims local models match Claude for complex vault operations. The gap is acknowledged but downplayed in privacy-focused sources.

**Vault separation philosophy:** Some sources strongly advocate complete vault separation (security, performance), while others suggest single-vault with folder separation is sufficient. No consensus on which scales better.

**Spaced repetition pricing:** True Recall's $120/year was challenged by community members noting free FSRS alternatives exist. Developer acknowledged the feedback as "the most valuable comment."

## Currency Assessment
- Most recent sources: February 2026 (Happy Coder, SRAI, mcp-obsidian-advanced)
- Topic velocity: Fast-moving for mobile and local AI; stable for spaced repetition
- Confidence in currency: High for mobile limitations, medium for local AI plugin landscape (new plugins appear frequently)

## Open Questions
- Will Claude Mobile ever support MCP protocol?
- Can local embedding models (nomic-embed-text, mxbai-embed-large) approach cloud quality for vault semantic search?
- What's the optimal strategy for migrating spaced repetition data between plugin architectures?
- How do corporate compliance requirements affect multi-vault AI configurations?
