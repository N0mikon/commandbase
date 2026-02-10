---
date: 2026-02-07
status: complete
topic: "Phase 5 Creating-Posts Skill Pre-Planning Research"
tags: [research, creating-posts, phase-5, content, social-media, voice-tone, skill-creation]
git_commit: 8e92bba
references:
  - .docs/future-skills/creating-posts.md
  - .docs/plans/02-07-2026-future-skills-implementation-roadmap.md
  - .docs/research/02-07-2026-anti-ai-voice-patterns-for-public-facing-content.md
  - ~/.claude/references/voice-tone-guide.md
  - newskills/brainstorming-code/SKILL.md
  - newskills/designing-code/SKILL.md
  - newskills/researching-repo/SKILL.md
archived: 2026-02-09
archive_reason: "Pre-planning research fully consumed. Skill implemented (8bb2b9e), deployed to plugins/commandbase-meta/skills/creating-posts/ (87a19a3). All open questions resolved. Referenced newskills/ paths moved to plugins/ during conversion; anti-AI voice research already archived."
---

# Phase 5 Creating-Posts Skill Pre-Planning Research

**Date**: 2026-02-07
**Branch**: master

## Research Question
What does a `/creating-posts` skill need — in terms of structure, dependencies, platform rules, modes, and integration points — to be ready for implementation planning?

## Summary
Phase 5 adds one skill (`/creating-posts`) that drafts human-sounding social media posts across 5 platforms (Reddit, Twitter/X, HN, LinkedIn, Discord). The skill has two modes: generate (draft from project context) and critique (rewrite AI-sounding user drafts). All dependencies are resolved — the voice/tone reference (`~/.claude/references/voice-tone-guide.md`, 116 lines) was completed in Phase 1b, and the anti-AI voice research (`.docs/research/02-07-2026-anti-ai-voice-patterns-for-public-facing-content.md`, 154 lines) provides the detection patterns. The skill follows the established 5-layer structure proven across Phases 2-4. This is classified as Low-Medium effort, 1 session.

## Detailed Findings

### 1. Resolved Dependencies

The roadmap (`.docs/plans/02-07-2026-future-skills-implementation-roadmap.md:341`) lists Phase 5 as depending on Phase 1b (voice/tone reference). This is complete:

- **Voice/Tone Reference** (`~/.claude/references/voice-tone-guide.md`, 116 lines): Three-tier word/phrase classification (20 Tier 1 banned words, 22 Tier 1 banned phrases, 49 Tier 2 strong avoidance words, Tier 3 contextual clustering rule), 7 structural writing rules, platform norms for Twitter/X + LinkedIn + GitHub, and a 3-question quick check.
- **Anti-AI Research** (`.docs/research/02-07-2026-anti-ai-voice-patterns-for-public-facing-content.md`, 154 lines): Cross-referenced 13+ sources, 140+ flagged words, structural uniformity patterns, platform-specific norms, humanization techniques with before/after examples, and 10 writing principles.

No other dependencies exist. Phase 5 is independent of Phase 4 (brainstorming) and can run in parallel with Phases 6-7.

### 2. Concept Document Analysis

The original concept (`.docs/future-skills/creating-posts.md`, 70 lines) defines:

**Core Behavior:**
- Takes context from codebase/README/conversation (line 13)
- Asks which platform (line 14)
- Drafts posts matching real platform voice (line 15)
- Provides 2-3 variants with different angles: technical, casual, problem-focused (line 16)
- Flags AI-sounding language and rewrites it (line 17)

**Platform Voice Table** (lines 23-29):
| Platform | Voice | Format |
|----------|-------|--------|
| Reddit | Casual, self-deprecating, honest about limitations | "I built X because Y was annoying" |
| Twitter/X | Punchy, thread-friendly, hot take energy | Short hook + thread |
| HN | Technical, understated, Show HN format | Problem + what's different + what's next |
| LinkedIn | Professional but not corporate | Brief, results-focused |
| Discord | Conversational, community-oriented | Short pitch + screenshot/link |

**Anti-Patterns** (lines 31-41): 9 specific phrases/behaviors to avoid.
**Good Post Examples** (lines 43-50): 6 authentic-sounding post formats.

**Open Questions from Concept** (lines 64-70):
1. Should it read README/CLAUDE.md or rely on user description? → **Resolved by roadmap: auto-reads project files** (roadmap:350)
2. Should it integrate with `/researching-web`? → **Not required for MVP; optional enhancement**
3. Platform character limits enforcement? → **Research needed: specific per-platform constraints**
4. Should it offer critique mode? → **Resolved by roadmap: yes, generate + critique** (roadmap:347)
5. Personal voice calibration? → **Partially resolved by voice/tone reference; may need per-user preference capture**

### 3. Roadmap Specification

From `.docs/plans/02-07-2026-future-skills-implementation-roadmap.md:340-356`:

**Requirements:**
- Draft social media posts that sound human-written (line 346)
- Generate + critique modes (line 347)
- Platform-aware: Reddit, Twitter/X, HN, LinkedIn, Discord (line 348)
- Anti-AI-voice enforcement using voice/tone reference (line 349)
- Auto-reads project files (README, CLAUDE.md, package.json) for context (line 350)

**Success Criteria** (lines 352-356):
1. `/creating-posts` deployed and tested
2. Produces natural-sounding posts for at least 2 platforms
3. Critique mode successfully identifies and rewrites AI-sounding language
4. Auto-reads project context without requiring user to describe the project

### 4. Skill Structure Template (from Phases 2-4)

Recent skills follow a proven 5-layer structure:

**Layer 1: YAML Frontmatter** (4 lines)
- `name:` matching directory name
- `description:` with trigger phrases and use cases

**Layer 2: Role Statement + Iron Law** (~20 lines)
- H1 title, role paragraph with "Violating the letter..." warning
- Code-fenced all-caps Iron Law directive
- "No exceptions:" bullet list (3-5 anti-patterns)

**Layer 3: Gate Function** (~15 lines)
- Code-fenced numbered checklist (5-9 steps)
- Steps use action verbs in all caps: READ, DETECT, DRAFT, VALIDATE, PRESENT
- Conditional logic where needed
- Consequence statement at end

**Layer 4: Process Flow** (~100 lines)
- Initial Response (conditional based on parameters)
- Step-by-step process with tool integrations
- Reference file pointers (`./reference/`, `./templates/`)
- docs-writer Task invocation for artifact creation

**Layer 5: Enforcement** (~40 lines)
- "Red Flags - STOP and [action]" section (5-7 bullet points)
- "Rationalization Prevention" table (Excuse | Reality, 5-7 rows)
- "The Bottom Line" (bold restatement + "Every [X]. Every time.")

**Supporting Files Pattern:**
- `reference/` — operational details, domain-specific templates
- `templates/` — output artifact format for docs-writer
- Referenced via relative paths: `./reference/filename.md`

**docs-writer Integration Pattern:**
```
Task prompt:
  doc_type: "<type>"
  topic: "<subject>"
  tags: [<relevant tags>]
  content: |
    <compiled output using ./templates/template-name.md>
```

### 5. Platform Constraints Research

Character limits and formatting rules per platform:

**Reddit:**
- Title: 300 characters max
- Self-post body: 40,000 characters max
- Markdown supported (bold, italic, links, code blocks)
- Subreddit-specific rules vary (r/selfhosted, r/sideproject, r/webdev have different norms)
- Flair often required

**Twitter/X:**
- 280 characters per tweet (Premium: 25,000 for long-form)
- Threads: unlimited tweets, each 280 chars
- 4 images, 1 video, or 1 GIF per tweet
- Links consume ~23 characters (t.co wrapping)
- No markdown — plain text only

**Hacker News:**
- Title: ~80 characters practical limit (renders poorly beyond)
- "Show HN:" prefix required for project showcases
- Body text: plain text only, no markdown, no images
- URLs auto-linked
- Community strongly prefers technical substance over marketing

**LinkedIn:**
- Post: 3,000 characters (truncation at ~210 for mobile feed)
- Article: 120,000 characters
- Markdown NOT supported (limited formatting: bold via Unicode, line breaks)
- Hashtags: 3-5 recommended, diminishing returns after
- First ~200 chars are the "hook" before "...see more"

**Discord:**
- Message: 2,000 characters
- Embed: 6,000 characters total
- Markdown supported (bold, italic, code blocks, spoilers)
- Server-specific channels may have different norms

### 6. Mode Design: Generate vs Critique

**Generate Mode (primary):**
1. Auto-read project context (README.md, CLAUDE.md, package.json)
2. Ask user: which platform? (AskUserQuestion with 5 options)
3. Ask user: what angle? (technical, casual, problem-focused, or let skill decide)
4. Draft 2-3 variants
5. Run each variant through voice/tone validation (Tier 1 scan, Tier 2 density, structural checks)
6. Present variants with any flagged issues highlighted
7. User selects or requests revision

**Critique Mode:**
1. User provides their draft text
2. Ask user: which platform is this for?
3. Scan for Tier 1 violations (flag exact phrases)
4. Scan for Tier 2 density (count and flag clusters)
5. Check Tier 3 clustering (3+ per paragraph rule)
6. Run structural checks (contractions, passive voice, sentence length variance, parallel construction)
7. Run 3-question quick check
8. Present findings with specific line-by-line rewrites
9. Offer to produce a full rewrite preserving the user's core message

### 7. Project Context Auto-Reading Strategy

The skill should auto-read project files to understand what to post about. Ordered by priority:

1. **README.md** — project description, features, what it does
2. **CLAUDE.md** — project structure, tech stack, directory layout
3. **package.json / Cargo.toml / pyproject.toml** — project name, version, description, dependencies
4. **CHANGELOG.md / RELEASES.md** — recent changes if posting about an update
5. **.docs/plans/** — current phase/progress if posting about journey

**Fallback behavior:**
- If none of these files exist (e.g., invoked outside a project directory), ask the user to describe what they're posting about
- If files exist but are sparse, supplement with questions

**What to extract:**
- Project name and one-line description
- Primary tech stack / language
- Key features (2-3 max for a post)
- What problem it solves
- Current status (MVP, beta, v1, mature)

### 8. Integration Points with Existing Skills

**Direct reference:**
- `~/.claude/references/voice-tone-guide.md` — the skill reads this for validation rules. NOT a copy — reads the live global file.

**No skill dependencies** (standalone invocation):
- Does NOT require `/researching-code` or `/brainstorming-code` to run first
- Does NOT produce artifacts consumed by downstream BRDSPI skills
- Output is conversation-only (no `.docs/` artifacts -- posts are ephemeral)

**Optional integration:**
- Could read `.docs/brainstorm/` artifacts if user recently brainstormed the feature (enhancement, not required)
- Could integrate with `/researching-web` to check competitor launch posts (enhancement, not required)

### 9. File Structure for the Skill

Based on the established pattern:

```
newskills/creating-posts/
├── SKILL.md                          # Main skill (~180-220 lines)
├── reference/
│   └── platform-guides.md            # Platform-specific voice, format, constraints
└── templates/
    └── post-output-template.md       # Output format for generated posts
```

**SKILL.md sections:**
1. YAML frontmatter (name, description with triggers)
2. Title + Role statement + Iron Law warning
3. The Iron Law: "NO POST WITHOUT VOICE VALIDATION"
4. The Gate Function (READ project → ASK platform → DRAFT → VALIDATE → PRESENT)
5. Initial Response (conditional: generate vs critique based on args)
6. Generate Mode process
7. Critique Mode process
8. Voice Validation process (reference to voice-tone-guide.md)
9. Important Guidelines
10. Red Flags - STOP and Rewrite
11. Rationalization Prevention
12. The Bottom Line

**reference/platform-guides.md:**
- Per-platform sections: voice, format constraints, character limits, good examples
- Subreddit-specific notes for Reddit
- Thread structure for Twitter/X
- Show HN format for HN
- Hook-first strategy for LinkedIn
- Server context for Discord

**templates/post-output-template.md:**
- Output format showing how variants are presented to user
- Validation summary section
- Platform-specific formatting notes

### 10. Decisions Already Made vs Open Questions

**Already decided (from roadmap + concept):**
- Two modes: generate + critique (roadmap:347)
- Five platforms: Reddit, Twitter/X, HN, LinkedIn, Discord (roadmap:348)
- Auto-reads project files for context (roadmap:350)
- Uses voice/tone reference for anti-AI enforcement (roadmap:349)
- 2-3 variants per generation (concept:16)
- Single skill, no sub-agents needed for generation (Low-Medium effort)

**Open questions for planning:**
1. **Output artifact location**: `.docs/posts/` seems right — but is it worth creating artifacts for social media posts, or just present in conversation? (Recommendation: present in conversation only, no docs-writer artifact — posts are ephemeral content, not development documentation)
2. **Personal voice calibration**: Voice/tone reference handles "not AI" but not "sounds like ME". Should the skill ask about personal voice preferences? (Recommendation: optional question "Any voice preferences?" with [Casual] [Technical] [Dry humor] [You decide] options — keep it lightweight)
3. **Subreddit targeting**: Reddit posts vary enormously by subreddit. Should the skill ask which subreddit? (Recommendation: yes, ask for subreddit when Reddit is selected — inform tone and flair requirements)
4. **Thread generation**: For Twitter/X, should it generate full threads or just the hook tweet? (Recommendation: offer both — [Single tweet] [Thread] as follow-up question)
5. **Model selection**: Design skills use opus. Does post generation benefit from opus? (Recommendation: no, default model is fine — this is creative writing, not architectural reasoning)

## Code References

- `.docs/future-skills/creating-posts.md:1-70` — Original concept document
- `.docs/plans/02-07-2026-future-skills-implementation-roadmap.md:340-356` — Phase 5 specification
- `.docs/plans/02-07-2026-future-skills-implementation-roadmap.md:500` — Session plan placement
- `.docs/plans/02-07-2026-future-skills-implementation-roadmap.md:513` — Quick win classification
- `.docs/research/02-07-2026-anti-ai-voice-patterns-for-public-facing-content.md:1-154` — Anti-AI voice research
- `~/.claude/references/voice-tone-guide.md:1-116` — Voice/tone reference (dependency)
- `newskills/brainstorming-code/SKILL.md:1-219` — Most recent skill structure reference
- `newskills/brainstorming-code/SKILL.md:147-156` — docs-writer integration pattern
- `newskills/brainstorming-code/SKILL.md:191-219` — Enforcement sections pattern
- `newskills/designing-code/SKILL.md:1-195` — Phase 2 skill structure reference
- `newskills/researching-repo/SKILL.md:1-224` — Phase 3 skill structure reference
- `newskills/discussing-features/SKILL.md:1-190` — Archived skill (preference capture patterns)
- `newskills/discussing-features/reference/question-domains.md:1-151` — Domain question template patterns

## Architecture Notes

- The skill is standalone — no BRDSPI chain position. It's a utility skill like `/committing-changes` or `/creating-prs`.
- Voice/tone validation should read `~/.claude/references/voice-tone-guide.md` at runtime, not embed a copy. This ensures updates to the guide propagate automatically.
- The 5-layer skill structure (frontmatter, role+iron law, gate function, process, enforcement) is well-proven across 4 phases. No structural innovation needed.
- Generate mode needs AskUserQuestion for platform and angle selection. Critique mode takes user text as input.
- No docs-writer integration recommended — posts are ephemeral conversation output, not `.docs/` artifacts. This breaks from the pattern of other skills but matches the content type.

## Open Questions (All Resolved During Implementation)

1. ~~Should posts be saved as `.docs/posts/` artifacts or presented in conversation only?~~ **Resolved: conversation only -- posts are ephemeral, no docs-writer artifact**
2. ~~Should the skill support custom subreddit targeting for Reddit?~~ **Resolved: yes, asks which subreddit when Reddit is selected**
3. ~~Should Twitter/X thread generation be a separate flow or integrated into the main generate mode?~~ **Resolved: integrated -- offers [Single tweet] or [Thread] as follow-up**
4. ~~Is personal voice calibration worth a preference question, or does "not AI" suffice?~~ **Resolved: skip -- platform defaults sufficient, user guides tone through description**
5. ~~Should the skill support other platforms beyond the initial 5 (e.g., Mastodon, Bluesky)?~~ **Resolved: deferred -- initial 5 only for MVP**
