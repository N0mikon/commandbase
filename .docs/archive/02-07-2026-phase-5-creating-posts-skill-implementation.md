---
date: 2026-02-07
status: complete
topic: "Phase 5 Creating-Posts Skill Implementation"
tags: [plan, implementation, creating-posts, phase-5, content, social-media, skill-creation]
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Bumped git_commit from 0c8fd24 (26 commits behind). Archive metadata and content verified accurate -- no content changes needed."
references:
  - .docs/archive/02-07-2026-phase-5-creating-posts-skill-pre-planning-research.md
  - .docs/future-skills/creating-posts.md
  - .docs/archive/02-07-2026-future-skills-implementation-roadmap.md
  - ~/.claude/references/voice-tone-guide.md
  - plugins/commandbase-meta/skills/creating-posts/SKILL.md
archived: 2026-02-09
archive_reason: "Completed plan superseded by plugin marketplace conversion. Skill migrated from newskills/creating-posts/ to plugins/commandbase-meta/skills/creating-posts/. Deployment model changed from manual copy to ~/.claude/skills/ to plugin install via marketplace. All implementation work finished; plan served its purpose."
---

# Phase 5: Creating-Posts Skill Implementation

## Overview

Create and deploy `/creating-posts` — a standalone utility skill that drafts human-sounding social media posts across 5 platforms (Reddit, Twitter/X, HN, LinkedIn, Discord) with generate + critique modes. Uses `~/.claude/references/voice-tone-guide.md` for anti-AI enforcement. Output is conversation-only (no `.docs/` artifacts).

**Effort:** Low-Medium | **Session:** 1 | **Files:** 3 new (SKILL.md + reference + template)

## Current State Analysis

**What exists:**
- Voice/tone reference (`~/.claude/references/voice-tone-guide.md`, 116 lines) — 3-tier word classification, 7 structural rules, platform norms, 3-question quick check
- Anti-AI research (`.docs/research/02-07-2026-anti-ai-voice-patterns-for-public-facing-content.md`, 154 lines) — 140+ flagged words, humanization techniques
- Concept document (`.docs/future-skills/creating-posts.md`, 70 lines) — platform voice table, anti-patterns, good examples
- Pre-planning research (`.docs/research/02-07-2026-phase-5-creating-posts-skill-pre-planning-research.md`) — full analysis with resolved open questions

**What doesn't exist:**
- `newskills/creating-posts/` directory
- Any deployed skill files at `~/.claude/skills/creating-posts/`

## Desired End State

```
newskills/creating-posts/
├── SKILL.md                          # Main skill (~200 lines)
├── reference/
│   └── platform-guides.md            # Per-platform voice, format, constraints (~120 lines)
└── templates/
    └── post-output-template.md       # Output format for presenting variants (~50 lines)
```

Deployed to `~/.claude/skills/creating-posts/` (same structure).

## What We're NOT Doing

- No `.docs/posts/` artifact creation — posts are ephemeral conversation output
- No docs-writer integration — unlike other skills, this one presents output inline
- No personal voice calibration question — platform default voice is sufficient
- No `/researching-web` integration — not required for MVP
- No additional platforms beyond the initial 5 (Mastodon, Bluesky deferred)
- No opus model — default model is fine for creative writing

## Design Decisions (Locked)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Output location | Conversation only | Posts are ephemeral; artifacts add overhead |
| Reddit subreddit | Ask when Reddit selected | r/selfhosted vs r/webdev norms differ significantly |
| Twitter/X threads | Offer [Single tweet] or [Thread] | Threads get 63% higher engagement |
| Voice preferences | Skip — use platform defaults | User can guide tone through description |
| Model | Default (not opus) | Creative writing, not architectural reasoning |
| Artifact creation | None | No docs-writer spawn |

## Implementation Phases

### Phase 1: Create reference/platform-guides.md (~120 lines)

Platform-specific reference containing voice, format constraints, character limits, and good examples for each of the 5 platforms.

**File:** `newskills/creating-posts/reference/platform-guides.md`

**Structure:**
```
# Platform Guides Reference

## Reddit
- Voice: Casual, self-deprecating, honest about limitations
- Format: Title (300 chars max) + self-post body (40,000 chars, markdown)
- Subreddit norms: r/selfhosted, r/sideproject, r/webdev, r/programming
- Good examples (3-4 authentic-sounding posts)
- Anti-patterns specific to Reddit

## Twitter/X
- Voice: Punchy, hot take energy, thread-friendly
- Format: 280 chars/tweet, links ~23 chars (t.co), plain text only
- Thread structure: Hook tweet → detail tweets → CTA tweet
- Good examples (single tweet + thread)
- Anti-patterns specific to Twitter/X

## Hacker News
- Voice: Technical, understated, substance over marketing
- Format: "Show HN:" prefix, ~80 char title, plain text body, no images
- Community norms: technical substance, no marketing language
- Good examples (Show HN format)
- Anti-patterns specific to HN

## LinkedIn
- Voice: Professional but not corporate, results-focused
- Format: 3,000 chars, ~200 char hook before truncation, no markdown
- Hashtags: 3-5 recommended
- Good examples (hook-first format)
- Anti-patterns specific to LinkedIn

## Discord
- Voice: Conversational, community-oriented
- Format: 2,000 chars, markdown supported
- Good examples (short pitch format)
- Anti-patterns specific to Discord
```

**Sources to draw from:**
- Concept document platform table (`.docs/future-skills/creating-posts.md:23-29`)
- Anti-AI research platform norms (`.docs/research/02-07-2026-anti-ai-voice-patterns-for-public-facing-content.md:74-102`)
- Voice/tone guide platform norms (`~/.claude/references/voice-tone-guide.md:84-106`)
- Pre-planning research platform constraints (research:131-167)

**Success criteria:**
- [x] All 5 platforms covered with voice, format, constraints, examples
- [x] Subreddit-specific guidance for Reddit (at least 4 subreddits)
- [x] Thread structure documented for Twitter/X
- [x] Character limits documented for all platforms
- [x] 2-4 good post examples per platform

### Phase 2: Create templates/post-output-template.md (~50 lines)

Template defining how generated posts are presented to the user in conversation.

**File:** `newskills/creating-posts/templates/post-output-template.md`

**Structure:**
```
# Post Output Template

## Generate Mode Output

Format for presenting 2-3 variants:

### Variant presentation format
- Platform header with constraints reminder
- Variant label (angle: technical/casual/problem-focused)
- The post text in a code fence (for easy copying)
- Character count vs limit
- Voice validation summary (pass/flagged items)

## Critique Mode Output

Format for presenting analysis of user's draft:
- Tier 1 violations (exact matches, mandatory fix)
- Tier 2 density (count, recommendation)
- Tier 3 clusters (paragraph-level check)
- Structural issues (contractions, passive voice, sentence length, parallel construction)
- Quick check results (3 questions)
- Suggested rewrite (full text preserving core message)

## Thread Output (Twitter/X only)

Format for presenting thread variants:
- Hook tweet (with char count)
- Detail tweets (numbered, with char counts)
- CTA tweet
- Total thread length
```

**Success criteria:**
- [x] Generate mode output format defined with variant labels and char counts
- [x] Critique mode output format covers all validation tiers
- [x] Thread-specific format for Twitter/X
- [x] Code fences used for easy copy-paste

### Phase 3: Write SKILL.md (~200 lines)

Main skill file following the 5-layer structure proven across Phases 2-4.

**File:** `newskills/creating-posts/SKILL.md`

**Section-by-section specification:**

**Layer 1: YAML Frontmatter (lines 1-4)**
```yaml
---
name: creating-posts
description: "Use this skill when drafting social media posts about projects, reviewing drafts for AI-sounding language, or creating platform-specific content. This includes generating posts for Reddit, Twitter/X, HN, LinkedIn, and Discord, critiquing existing drafts for anti-AI voice compliance, and auto-reading project context for content. Trigger phrases: '/creating-posts', 'write a post', 'draft a tweet', 'critique my post', 'review this draft'."
---
```

**Layer 2: Title + Role + Iron Law (lines 6-25)**
- H1: "# Creating Posts"
- Role paragraph: drafting human-sounding social media posts, two modes (generate + critique), platform-aware, uses voice/tone reference
- "Violating the letter of these rules is violating the spirit of these rules."
- Iron Law: `NO POST WITHOUT VOICE VALIDATION`
- Explanation: Every draft — generated or critiqued — must pass voice/tone validation before presenting to user. No "looks fine to me" shortcuts.
- "No exceptions:" list (4 items):
  - Don't skip validation for short posts — short posts are MORE visible
  - Don't present drafts without checking Tier 1 bans — one "delve" ruins credibility
  - Don't generate without reading project context first — context-free posts are generic
  - Don't assume platform voice — read `./reference/platform-guides.md` for THIS platform

**Layer 3: Gate Function (lines 27-42)**
```
BEFORE presenting any post to the user:

1. READ: Auto-read project context (README.md, CLAUDE.md, package.json)
2. DETECT: Generate mode or Critique mode?
3. ASK: Which platform? (+ subreddit for Reddit, + single/thread for Twitter/X)
4. DRAFT: Generate 2-3 variants (generate) or analyze draft (critique)
5. VALIDATE: Run voice/tone check against ~/.claude/references/voice-tone-guide.md
6. FIX: Rewrite any flagged issues before presenting
7. ONLY THEN: Present to user

Skipping validation = presenting AI-sounding content = defeating the purpose
```

**Layer 4: Process Flow (lines 44-160)**

**Initial Response (lines 44-70)**

Three conditional paths:
1. If "critique" or user's draft text provided as argument → enter Critique Mode
2. If project context or topic provided as argument → enter Generate Mode
3. If no argument → present mode selection:
```
I'll help you create a social media post.

What would you like to do?
1. Generate a post about this project (I'll read the codebase for context)
2. Critique a draft you've already written

Or provide your draft text directly and I'll review it.
```

**Generate Mode (lines 72-120)**

Step 1: Read Project Context
- Attempt to read (in order): README.md, CLAUDE.md, package.json / Cargo.toml / pyproject.toml
- Extract: project name, one-line description, tech stack, key features (2-3), what problem it solves, current status
- If no project files found → ask user to describe what they're posting about
- If sparse → supplement with targeted questions

Step 2: Platform Selection
- Use AskUserQuestion with 5 options: [Reddit] [Twitter/X] [Hacker News] [LinkedIn] [Discord]
- If Reddit selected → follow-up: "Which subreddit?" with [r/selfhosted] [r/sideproject] [r/webdev] [r/programming] + Other
- If Twitter/X selected → follow-up: "Format?" with [Single tweet] [Thread]

Step 3: Draft Variants
- Read `./reference/platform-guides.md` for selected platform's voice, format, constraints
- Generate 2-3 variants with different angles (technical, casual, problem-focused)
- Apply platform-specific formatting (character limits, markdown/plain text, Show HN prefix, etc.)

Step 4: Voice Validation
- Read `~/.claude/references/voice-tone-guide.md`
- For each variant:
  - Scan for Tier 1 banned words and phrases → rewrite before presenting (mandatory)
  - Count Tier 2 words → flag if >2 per variant
  - Check Tier 3 clustering → flag if 3+ per paragraph
  - Run structural checks: contractions present, active voice, sentence length variance, no parallel construction overuse
- Fix all Tier 1 violations automatically. Flag Tier 2/3 for user awareness.

Step 5: Present Variants
- Use format from `./templates/post-output-template.md`
- Present each variant with: angle label, the post text in a code fence, character count, validation summary
- Ask: "Want to use one of these, adjust one, or try different angles?"

**Critique Mode (lines 122-150)**

Step 1: Receive Draft
- User provides their draft text (via argument or paste)

Step 2: Platform Context
- Use AskUserQuestion: "Which platform is this for?" with [Reddit] [Twitter/X] [Hacker News] [LinkedIn] [Discord] [General]

Step 3: Voice Analysis
- Read `~/.claude/references/voice-tone-guide.md`
- Tier 1 scan: flag exact word/phrase matches with line references from the guide
- Tier 2 density: count occurrences, flag if >2
- Tier 3 clustering: check paragraph-by-paragraph
- Structural analysis: contractions, passive voice, sentence length variance, parallel constructions, hedging clusters
- Run 3-question quick check:
  1. Would you say this aloud to a colleague?
  2. Does it include at least one specific example?
  3. Is it jargon-free?

Step 4: Present Findings
- Use critique format from `./templates/post-output-template.md`
- Show issues grouped by severity (Tier 1 → Tier 2 → Tier 3 → Structural)
- For each issue: quote the flagged text, explain why, suggest rewrite
- Offer full rewrite preserving core message

**Layer 5: Enforcement (lines 162-200)**

**Important Guidelines (lines 162-175)**
1. Always read project context before generating — never draft from thin air
2. Platform voice comes from `./reference/platform-guides.md`, NOT from memory
3. Voice validation reads the live file at `~/.claude/references/voice-tone-guide.md` every time — never cache
4. Tier 1 violations are fixed automatically, not flagged — the user should never see a "delve" in a variant
5. Code fences for post text — makes copy-paste easy
6. Character counts are mandatory — user needs to know if it fits

**Red Flags - STOP and Rewrite (lines 177-188)**
- Presenting a variant without running voice validation
- Using words from the Tier 1 banned list in generated text
- Generating without reading project context first
- Applying the wrong platform's voice (LinkedIn tone on a Reddit post)
- Skipping character count or exceeding platform limits
- Generating only 1 variant (minimum 2)
- Presenting critique results without offering a rewrite

**Rationalization Prevention (lines 190-198)**

| Excuse | Reality |
|--------|---------|
| "This post is too short to validate" | Short posts are MORE visible. Validate everything. |
| "I already know the voice/tone rules" | Read the guide file. Every time. Rules may have been updated. |
| "One variant is enough, it's good" | Minimum 2 variants. Users deserve choices. |
| "The user's draft looks fine" | Run the checks. Humans miss their own AI-sounding patterns. |
| "This platform doesn't need specific voice" | Every platform has norms. Read the platform guide. |

**The Bottom Line (lines 200-204)**

**No post without voice validation.**

Read the project. Ask the platform. Draft the variants. Validate against the guide. Fix Tier 1 violations. THEN present.

This is non-negotiable. Every post. Every time.

### Phase 4: Deploy and Verify

**Actions:**
1. Create `~/.claude/skills/creating-posts/` directory structure
2. Copy all 3 files:
   - `newskills/creating-posts/SKILL.md` → `~/.claude/skills/creating-posts/SKILL.md`
   - `newskills/creating-posts/reference/platform-guides.md` → `~/.claude/skills/creating-posts/reference/platform-guides.md`
   - `newskills/creating-posts/templates/post-output-template.md` → `~/.claude/skills/creating-posts/templates/post-output-template.md`
3. Verify skill appears in available skills list (may require Claude Code restart)
4. Test generate mode: invoke `/creating-posts` in a real project, verify it reads context and produces variants
5. Test critique mode: provide a deliberately AI-sounding draft, verify it catches issues

**Success criteria:**
- [x] Skill appears in Claude Code's available skills
- [ ] Generate mode auto-reads project files and produces 2-3 variants (requires functional test)
- [ ] Critique mode identifies Tier 1 violations and suggests rewrites (requires functional test)
- [ ] Character counts displayed for all variants (requires functional test)
- [ ] Platform-specific voice applied correctly (requires functional test)

### Phase 5: Update Roadmap

**Actions:**
1. Edit `.docs/plans/02-07-2026-future-skills-implementation-roadmap.md`:
   - Mark Phase 5 success criteria checkboxes as complete (lines 352-356)
   - Update complexity summary table status (line 481)
   - Update session plan (line 500)
   - Update quick reference dependency table (line 468)
2. Check if any `.docs/` files reference Phase 5 as "not started" and update

**Success criteria:**
- [x] All 4 Phase 5 success criteria checked in roadmap
- [x] Phase 5 status updated from "Not started" to "COMPLETE" in all tables

## Testing Strategy

**Generate Mode Test:**
1. Invoke `/creating-posts` in the `commandbase` project (has README.md and CLAUDE.md)
2. Select Reddit + r/selfhosted
3. Verify: 2-3 variants produced, casual voice, character counts shown, no Tier 1 words
4. Select Twitter/X + Thread
5. Verify: hook tweet + detail tweets produced, each within 280 chars

**Critique Mode Test:**
1. Provide this deliberately AI-sounding draft:
   ```
   I'm thrilled to announce the launch of my groundbreaking tool that leverages
   cutting-edge technology to seamlessly optimize your workflow. In today's
   fast-paced world, it's important to note that this robust solution delves
   deep into the complexities of modern development.
   ```
2. Verify: Tier 1 violations caught ("thrilled", "groundbreaking", "leverages", "cutting-edge", "seamlessly", "optimize", "In today's fast-paced world", "it's important to note", "robust", "delves", "complexities")
3. Verify: rewrite offered that preserves core message

## Migration Notes

- No existing skill to migrate from
- `/discussing-features` retirement was handled in Phase 4 — no overlap with this skill
- Voice/tone reference is read-only from the skill's perspective — no modifications needed
- Skill is completely standalone — no integration with BRDSPI chain
