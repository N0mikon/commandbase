# Social Media Posts (`/creating-posts`)

> **Status: IMPLEMENTED** -- Deployed in Phase 5 (2026-02-07). Skill lives at `newskills/creating-posts/` and `~/.claude/skills/creating-posts/`. All open questions below were resolved during implementation. See `.docs/plans/02-07-2026-phase-5-creating-posts-skill-implementation.md` for full details.

## Problem

AI-generated project announcements are instantly recognizable and actively hurt credibility. Reddit, Twitter/X, and Hacker News are flooded with posts that read like ChatGPT wrote them — "I'm excited to announce...", "leveraging the power of...", "after countless hours...". The community has developed antibodies. A genuine project shared with AI-sounding copy gets dismissed before anyone looks at the work.

## Concept

A skill that drafts social media posts about your projects that sound like a human wrote them. Not by hiding that AI helped — by actually writing the way real developers talk about their work.

### What It Does

- Takes context about what you built (from codebase, README, or conversation)
- Asks which platform (Reddit, Twitter/X, HN, LinkedIn, Discord)
- Drafts a post in a voice that matches how real people write on that platform
- Provides 2-3 variants with different angles (technical, casual, problem-focused)
- Flags anything that sounds AI-generated and rewrites it

### Platform Awareness

Each platform has different norms:

| Platform | Voice | Format |
|---|---|---|
| Reddit | Casual, self-deprecating, honest about limitations | "I built X because Y was annoying. Here's what I learned." |
| Twitter/X | Punchy, thread-friendly, hot take energy | Short hook + thread with details |
| Hacker News | Technical, understated, Show HN format | Problem statement + what's different + what's next |
| LinkedIn | Professional but not corporate | Brief, results-focused, no buzzwords |
| Discord | Conversational, community-oriented | Short pitch + screenshot/link |

### Anti-Patterns to Actively Avoid

- "I'm thrilled/excited to share..."
- "After countless hours of hard work..."
- "Leveraging the power of..."
- "Game-changing", "revolutionary", "seamless"
- "In today's fast-paced world..."
- Bullet points listing features nobody asked about
- Starting with a question nobody was asking ("Ever struggled with...?")
- Emoji spam
- "Let me know what you think!" (begging for engagement)

### What Good Posts Actually Sound Like

- "I got tired of X so I built Y. It's rough but it works."
- "Shipping this before I talk myself out of it. [link]"
- "Show HN: [thing] — does [specific thing] without [annoying thing]"
- Leading with the problem, not the solution
- Honest about scope — what it does, what it doesn't do yet
- Specific details over vague claims

## Broader Application

The anti-AI-voice research and anti-patterns aren't just for social media posts. The same problem shows up anywhere Claude generates text that humans will read. Consider incorporating this work into:

- **README.md generation** — project READMEs written by AI are just as recognizable as social media posts
- **`/creating-prs`** — PR descriptions that sound human and useful vs templated AI boilerplate
- **`/handing-over`** — handoff docs that read like a person wrote them for another person
- **`/committing-changes`** — commit messages that sound like a developer, not a press release

Could be a shared reference (voice/tone guide in `~/.claude/references/`) that multiple skills pull from, rather than duplicating anti-pattern lists across every skill. Lives in global config alongside skills and agents — not `.docs/` which is project-scoped and ephemeral. Single source of truth avoids mirrored copies drifting out of sync across skills.

## Open Questions (All Resolved)

- ~~Should it read the project's README/CLAUDE.md for context, or rely on user description?~~ **Resolved: auto-reads project files (README.md, CLAUDE.md, package.json), falls back to asking user**
- ~~Should it integrate with `/researching-web` to check what similar projects said when they launched (and avoid sounding the same)?~~ **Resolved: not required for MVP, deferred as optional enhancement**
- ~~Platform-specific character limits and formatting — how much should it enforce?~~ **Resolved: character limits enforced per platform, documented in `reference/platform-guides.md`**
- ~~Should it offer to critique a draft the user already wrote, in addition to generating from scratch?~~ **Resolved: yes, generate + critique modes implemented**
- ~~Tone calibration — how does the user communicate their personal voice vs just "not AI"?~~ **Resolved: platform default voice sufficient, user can guide tone through description**
