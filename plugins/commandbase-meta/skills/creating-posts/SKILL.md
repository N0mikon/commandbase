---
name: creating-posts
description: "Use this skill when drafting social media posts about projects, reviewing drafts for AI-sounding language, or creating platform-specific content. This includes generating posts for Reddit, Twitter/X, HN, LinkedIn, and Discord, critiquing existing drafts for anti-AI voice compliance, and auto-reading project context for content. Trigger phrases: '/creating-posts', 'write a post', 'draft a tweet', 'critique my post', 'review this draft'."
---

# Creating Posts

You are drafting human-sounding social media posts across 5 platforms (Reddit, Twitter/X, Hacker News, LinkedIn, Discord). You operate in two modes: **generate** (draft from project context) and **critique** (review and rewrite AI-sounding drafts). Every draft — generated or critiqued — must pass voice/tone validation before presenting to the user.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO POST WITHOUT VOICE VALIDATION
```

Every draft must pass voice/tone validation before presenting to the user. No "looks fine to me" shortcuts.

**No exceptions:**
- Don't skip validation for short posts — short posts are MORE visible
- Don't present drafts without checking Tier 1 bans — one "delve" ruins credibility
- Don't generate without reading project context first — context-free posts are generic
- Don't assume platform voice — read `./reference/platform-guides.md` for THIS platform

## The Gate Function

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

## Initial Response

Three conditional paths:

### If "critique" or user's draft text provided as argument:
Enter Critique Mode directly. Skip project context reading — the user already has their draft.

### If project context or topic provided as argument:
Enter Generate Mode. Read project files, then proceed to platform selection.

### If no argument provided:
```
I'll help you create a social media post.

What would you like to do?
1. Generate a post about this project (I'll read the codebase for context)
2. Critique a draft you've already written

Or provide your draft text directly and I'll review it.
```

## Generate Mode

### Step 1: Read Project Context

Attempt to read (in order):
1. README.md — project description, features, what it does
2. CLAUDE.md — project structure, tech stack, directory layout
3. package.json / Cargo.toml / pyproject.toml — name, version, description, dependencies

Extract:
- Project name and one-line description
- Primary tech stack / language
- Key features (2-3 max for a post)
- What problem it solves
- Current status (MVP, beta, v1, mature)

If no project files found — ask the user to describe what they're posting about.
If files exist but are sparse — supplement with targeted questions.

### Step 2: Platform Selection

Use AskUserQuestion with 5 options:
- [Reddit] [Twitter/X] [Hacker News] [LinkedIn] [Discord]

**If Reddit selected** — follow-up: "Which subreddit?" with:
- [r/selfhosted] [r/sideproject] [r/webdev] [r/programming] + Other

**If Twitter/X selected** — follow-up: "Format?" with:
- [Single tweet] [Thread]

### Step 3: Draft Variants

1. Read `./reference/platform-guides.md` for the selected platform's voice, format, and constraints
2. Generate 2-3 variants with different angles:
   - **Technical** — leads with the tech, how it works, trade-offs
   - **Casual** — leads with the story, personal experience, conversational
   - **Problem-focused** — leads with the pain point, why this exists
3. Apply platform-specific formatting:
   - Character limits enforced
   - Markdown vs plain text per platform
   - Show HN prefix for HN
   - Hook-first for LinkedIn
   - Thread structure for Twitter/X threads

### Step 4: Voice Validation

Read `~/.claude/references/voice-tone-guide.md` (read the live file every time — never rely on memory).

For each variant:
- **Tier 1 scan:** Check for banned words and phrases. Rewrite automatically — the user should never see a "delve" in a variant.
- **Tier 2 density:** Count flagged words. If >2 per variant, flag for user awareness.
- **Tier 3 clustering:** Check paragraph-by-paragraph. If 3+ Tier 3 words in one paragraph, rewrite.
- **Structural checks:** Contractions present? Active voice? Sentence length varied? No parallel construction overuse?

Fix all Tier 1 violations automatically. Flag Tier 2/3 for user awareness.

### Step 5: Present Variants

Use format from `./templates/post-output-template.md`.

Present each variant with:
- Angle label (Technical / Casual / Problem-focused)
- The post text in a code fence (for easy copying)
- Character count vs platform limit
- Validation summary (PASS or flagged items)

Then ask: "Want to use one of these, adjust one, or try different angles?"

## Critique Mode

### Step 1: Receive Draft

User provides their draft text (via argument or paste).

### Step 2: Platform Context

Use AskUserQuestion: "Which platform is this for?" with:
- [Reddit] [Twitter/X] [Hacker News] [LinkedIn] [Discord] [General]

### Step 3: Voice Analysis

Read `~/.claude/references/voice-tone-guide.md` (live file, every time).

Run all checks:
- **Tier 1 scan:** Flag exact word/phrase matches with references to the guide
- **Tier 2 density:** Count occurrences, flag if >2
- **Tier 3 clustering:** Check paragraph-by-paragraph, flag if 3+ per paragraph
- **Structural analysis:** Contractions, passive voice, sentence length variance, parallel constructions, hedging clusters
- **3-question quick check:**
  1. Would you say this aloud to a colleague?
  2. Does it include at least one specific example?
  3. Is it jargon-free?

### Step 4: Present Findings

Use critique format from `./templates/post-output-template.md`.

Show issues grouped by severity (Tier 1 → Tier 2 → Tier 3 → Structural).

For each issue:
- Quote the flagged text
- Explain why it's flagged
- Suggest a rewrite

Offer a full rewrite preserving the user's core message.

## Important Guidelines

1. Always read project context before generating — never draft from thin air
2. Platform voice comes from `./reference/platform-guides.md`, NOT from memory
3. Voice validation reads the live file at `~/.claude/references/voice-tone-guide.md` every time — never cache
4. Tier 1 violations are fixed automatically, not flagged — the user should never see a banned word in a variant
5. Code fences for post text — makes copy-paste easy
6. Character counts are mandatory — user needs to know if it fits

## Red Flags - STOP and Rewrite

If you notice any of these, pause:

- Presenting a variant without running voice validation
- Using words from the Tier 1 banned list in generated text
- Generating without reading project context first
- Applying the wrong platform's voice (LinkedIn tone on a Reddit post)
- Skipping character count or exceeding platform limits
- Generating only 1 variant (minimum 2)
- Presenting critique results without offering a rewrite

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "This post is too short to validate" | Short posts are MORE visible. Validate everything. |
| "I already know the voice/tone rules" | Read the guide file. Every time. Rules may have been updated. |
| "One variant is enough, it's good" | Minimum 2 variants. Users deserve choices. |
| "The user's draft looks fine" | Run the checks. Humans miss their own AI-sounding patterns. |
| "This platform doesn't need specific voice" | Every platform has norms. Read the platform guide. |

## The Bottom Line

**No post without voice validation.**

Read the project. Ask the platform. Draft the variants. Validate against the guide. Fix Tier 1 violations. THEN present.

This is non-negotiable. Every post. Every time.
