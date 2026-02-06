# Claude Opus 4.6 vs Opus 4.5: Changes and Improvements

**Date**: February 5, 2026
**Query**: What changed in Opus 4.6 compared to Opus 4.5?
**Agents**: 4 parallel web-researcher agents (official announcement, benchmarks, community reactions, technical details)

## TL;DR

Opus 4.6 launched February 5, 2026. Major upgrades: 1M token context window (5x increase), 128K output tokens (2x), adaptive thinking, agent teams, and massive benchmark gains in reasoning/coding. Same pricing as 4.5. Trade-off: community reports degraded writing/prose quality. Use 4.6 for coding, 4.5 for writing is the emerging consensus.

---

## Key Changes at a Glance

| Feature | Opus 4.5 | Opus 4.6 |
|---------|-----------|-----------|
| Context window | 200K tokens | 200K standard / **1M beta** |
| Max output | 64K tokens | **128K tokens** |
| Thinking | Extended thinking (manual) | **Adaptive thinking** (automatic) |
| Agent coordination | Single agent | **Agent teams** (multi-agent) |
| Context management | Manual | **Context compaction** (auto-summarization) |
| Effort control | N/A | **4 levels** (low/medium/high/max) |
| Pricing (input/output) | $5/$25 per MTok | $5/$25 per MTok (unchanged) |
| Knowledge cutoff | Early 2025 | May 2025 (reliable) / Aug 2025 (training) |
| Model ID | `claude-opus-4-5-20250929` | `claude-opus-4-6` |

## Benchmark Comparisons

### Massive Improvements

| Benchmark | Opus 4.5 | Opus 4.6 | Change |
|-----------|----------|----------|--------|
| **ARC-AGI-2** (abstract reasoning) | 37.6% | **68.8%** | +83% (nearly doubled) |
| **MRCR v2** (long-context retrieval, 1M) | 18.5% | **76%** | ~4x improvement |
| **GDPval-AA** (knowledge work) | 1416 Elo | **1606 Elo** | +190 Elo points |
| **GPQA Diamond** (grad-level reasoning) | 87.0% | **91.3%** | +4.3 points |
| **Terminal-Bench 2.0** (agentic coding) | 59.8% | **65.4%** | +5.6 points |
| **OSWorld** (computer use) | 66.3% | **72.7%** | +6.4 points |

### Parity / Slight Regression

| Benchmark | Opus 4.5 | Opus 4.6 | Notes |
|-----------|----------|----------|-------|
| **SWE-bench Verified** | 80.9% | 80.8% | Slight regression (-0.1%) |

### New Benchmarks (no 4.5 comparison available)

- **Humanity's Last Exam**: 53.1% (leads all frontier models)
- **BrowseComp**: 84.0% (best for finding hard-to-find information)
- **BigLaw Bench**: 90.2% (highest Claude score, legal reasoning)
- **Aider Polyglot**: 89.4%
- **SWE-bench Multilingual**: Leading on 7 of 8 languages

### Competitive Context

- **vs GPT-5.2**: Opus 4.6 leads on ARC-AGI-2, Terminal-Bench 2.0, GDPval-AA, BrowseComp; trails on GPQA Diamond
- **vs Gemini 3 Pro**: Opus 4.6 leads across most benchmarks
- **Note**: OpenAI released GPT-5.3-Codex 20 minutes after Opus 4.6, beating it on Terminal-Bench 2.0 (77.3% vs 65.4%)

## New Features

### Adaptive Thinking
- Replaces manual `thinking: {type: "enabled"}` with `thinking: {type: "adaptive"}`
- Model dynamically decides when and how much to reason based on task complexity
- Four effort levels: low, medium, high (default), max
- Interleaved thinking automatically enabled

### Agent Teams (Research Preview)
- Multiple AI agents work simultaneously on different aspects of a coding project
- Autonomous coordination between agents
- Available in Claude Code

### Context Compaction
- Automatic server-side context summarization
- Enables effectively infinite conversations without hitting limits
- Addresses "context rot" - performance degradation in long conversations

### 1M Token Context Window (Beta)
- Activated with `context-1m-2025-08-07` beta header
- Long-context pricing: $10 input / $37.50 output per MTok (for prompts >200K)
- First Opus-class model with 1M context

### 128K Output Tokens
- Doubled from 64K limit
- Enables longer thinking budgets and more comprehensive responses

## API Breaking Changes

- **Prefilling assistant messages**: No longer supported, returns 400 error
- **`output_format`**: Moved to `output_config.format` (deprecated)
- **`budget_tokens`**: Removed in favor of adaptive thinking
- **JSON string escaping**: May differ slightly from previous versions

## Community Reception

### Positive
- Coding capabilities praised by developers and industry professionals
- Michael Truell (Cursor): "Greater persistence, stronger code review, ability to stay on long tasks"
- Mario Rodriguez (GitHub): "Unlocking long-horizon tasks previously achievable only by humans"
- Zero-day discovery: Found 500+ previously unknown vulnerabilities in open-source code
- Hacker News: 962 upvotes, 193 comments, memory features praised

### Negative / Concerns
- **Writing quality degradation**: Most prominent complaint
  - Reddit: "Opus 4.6 lobotomized" (167 upvotes), "Opus 4.6 nerfed?" (81 upvotes) - within hours of release
  - Every.to blind test: Team preferred Opus 4.5's prose over 4.6
  - More prone to "AI-isms" like "X not Y" constructions
  - Theory: RLHF optimizations for reasoning degraded prose quality
- **Speed**: Significantly slower than Opus 4.5
- **More verbose**: Outputs tend to be longer
- **Unexpected code changes**: Makes modifications without clear justification
- **Prompt injection**: "Slightly more vulnerable to indirect prompt injections than predecessor"
- **Windows bugs**: Critical issue making Claude Code nearly unusable (EBUSY file lock, unresponsive tabs)

### Emerging Consensus
- **Use Opus 4.6 for**: Coding, agentic tasks, complex reasoning, long-context work
- **Use Opus 4.5 for**: Writing, creative work, prose-heavy tasks

## Pricing

| Tier | Input | Output |
|------|-------|--------|
| Standard | $5/MTok | $25/MTok |
| Long context (>200K) | $10/MTok | $37.50/MTok |
| Batch API | $2.50/MTok | $12.50/MTok |
| Prompt caching (5min write) | $6.25/MTok | - |
| Prompt caching (1hr write) | $10/MTok | - |
| Prompt caching (hit) | $0.50/MTok | - |
| US-only inference | 1.1x multiplier | 1.1x multiplier |

## Platform Availability

- claude.ai (Pro, Max, Team, Enterprise)
- Claude API (direct)
- Amazon Bedrock (`anthropic.claude-opus-4-6-v1`)
- Google Cloud Vertex AI (`claude-opus-4-6`)
- Microsoft Foundry (Azure)
- GitHub Copilot
- Claude in PowerPoint (research preview)
- Claude in Excel (enhanced)

## Conflicts Between Sources

1. **Writing quality**: Official sources make no mention of degradation; community reports it immediately. Every.to confirmed it with blind testing.
2. **"No regressions"**: Cosmic comparison found no regressions; Reddit/HN users strongly disagree for prose tasks.
3. **Developer testimonials vs community**: Professional endorsements overwhelmingly positive while community forums show frustration - suggests bifurcation between enterprise coding users and creative/writing users.

## Sources

### Official
- [Introducing Claude Opus 4.6 - Anthropic](https://www.anthropic.com/news/claude-opus-4-6)
- [What's New in Claude 4.6 - Platform Docs](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6)
- [Models Overview - Platform Docs](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Pricing - Platform Docs](https://platform.claude.com/docs/en/about-claude/pricing)
- [System Card PDF](https://www-cdn.anthropic.com/0dd865075ad3132672ee0ab40b05a53f14cf5288.pdf)

### Press Coverage
- [TechCrunch - Agent Teams](https://techcrunch.com/2026/02/05/anthropic-releases-opus-4-6-with-new-agent-teams/)
- [CNBC - Vibe Working](https://www.cnbc.com/2026/02/05/anthropic-claude-opus-4-6-vibe-working.html)
- [VentureBeat - 1M Token Context](https://venturebeat.com/technology/anthropics-claude-opus-4-6-brings-1m-token-context-and-agent-teams-to-take)
- [The New Stack - Enterprise Step Change](https://thenewstack.io/anthropics-opus-4-6-is-a-step-change-for-the-enterprise/)
- [Fast Company - Bigger Codebases](https://www.fastcompany.com/91488000/anthropics-new-claude-opus-4-6-aims-to-think-through-bigger-codebases)
- [Axios - 500 Zero-Day Flaws](https://www.axios.com/2026/02/05/anthropic-claude-opus-46-software-hunting)

### Community & Reviews
- [Hacker News Discussion (962 points)](https://news.ycombinator.com/item?id=46902223)
- [WinBuzzer - Coding vs Writing Trade-off](https://winbuzzer.com/2026/02/05/claude-opus-4-6-coding-writing-tradeoff-xcxwbn/)
- [Every.to - Vibe Check](https://every.to/vibe-check/opus-4-6)
- [Cosmic - Real-World Comparison](https://www.cosmicjs.com/blog/claude-opus-46-vs-opus-45-a-real-world-comparison)
- [Cursor Forum Discussion](https://forum.cursor.com/t/claude-4-6-opus-out-now/150946)

### Platform Availability
- [AWS Bedrock](https://aws.amazon.com/about-aws/whats-new/2026/2/claude-opus-4.6-available-amazon-bedrock/)
- [Google Vertex AI](https://cloud.google.com/blog/products/ai-machine-learning/expanding-vertex-ai-with-claude-opus-4-6/)
- [GitHub Copilot](https://github.blog/changelog/2026-02-05-claude-opus-4-6-is-now-generally-available-for-github-copilot/)
- [Microsoft Foundry / Azure](https://azure.microsoft.com/en-us/blog/claude-opus-4-6-anthropics-powerful-model-for-coding-agents-and-enterprise-workflows-is-now-available-in-microsoft-foundry-on-azure/)

### Benchmarks & Analysis
- [DataCamp - Features & Benchmarks](https://www.datacamp.com/blog/claude-opus-4-6)
- [OfficeChai - Benchmark Breakdown](https://officechai.com/ai/claude-opus-4-6-benchmarks-released/)
- [Digital Applied - Pricing Guide](https://www.digitalapplied.com/blog/claude-opus-4-6-release-features-benchmarks-guide)
- [The Decoder - 1M Context Window](https://the-decoder.com/claude-opus-4-6-brings-one-million-token-context-window-to-anthropics-flagship-model/)
