---
date: 2026-02-07
status: complete
topic: "Anti-AI Voice Patterns for Public-Facing Content"
tags: [research, voice-tone, anti-ai-voice, social-media, github, writing-style]
git_commit: 5beb0c1
references:
  - ~/.claude/references/voice-tone-guide.md
  - .docs/plans/02-07-2026-future-skills-implementation-roadmap.md
---

# Anti-AI Voice Patterns for Public-Facing Content

## Research Question
What specific words, phrases, structural patterns, and platform norms should a voice/tone reference guide address to prevent AI-generated text from sounding robotic or detectable?

## Summary
Cross-referenced 13+ sources from 2025-2026 including GPTZero analysis, academic studies (Stanford, Frontiers in Education), editorial checklists, and platform-specific guides. AI text is detectable through vocabulary markers (140+ flagged words), structural uniformity (sentence length clustering, parallel lists), hedging patterns, and missing human elements (contractions, personality, slang). GitHub PR reviewers report 1.7x more defects in AI-generated code with 3x readability issues.

## Detailed Findings

### Tier 1: Absolute Bans (Strongest AI Signals)

**Words that scream AI (10x+ more frequent in AI text per GPTZero):**
- "Delve" (15% of ChatGPT responses)
- "Tapestry" (8% of creative outputs)
- "Leverage" / "Utilize" (formal alternatives to "use")
- "Landscape" / "Realm" / "Beacon"
- "Embark on a journey" (14% of narrative starts)
- "Testament to" (12% of essays)
- "Plays a significant role in shaping" (182x more frequent in AI)

**Phrases that are instant flags:**
- "In the ever-evolving landscape of..."
- "In today's fast-paced world" (107x more in AI)
- "It's important to note that..."
- "It's worth noting that..."
- "At the forefront of..."
- "Unlock/Unleash the potential of..."
- "In conclusion..."
- "Let's delve into..."

### Tier 2: Strong Avoidance (High AI Correlation)

**Adjectives:** Robust, Comprehensive, Nuanced, Multifaceted, Intricate, Compelling, Pivotal, Paramount, Innovative, Cutting-edge, Seamless, Groundbreaking, Holistic, Revolutionary, Dynamic

**Verbs:** Foster, Navigate, Unpack, Harness, Underscore, Exemplify, Facilitate, Optimize, Streamline, Embark, Enhance, Reinforce

**Nouns:** Cornerstone, Plethora, Myriad, Spectrum, Facet, Framework, Ecosystem, Paradigm, Synergy, Discourse

**Transitions:** Furthermore, Moreover, Additionally, Nevertheless, Consequently, Subsequently, Accordingly

### Tier 3: Contextual Avoidance (Fine in Moderation)

These are normal English words that only flag when overused or clustered:
- "Significant", "Notable", "Effective" — fine alone, suspicious in groups
- "Therefore", "Thus", "Hence" — fine in technical writing, suspicious in social posts
- "Navigate", "Drive", "Enhance" — fine as literal verbs, suspicious as metaphors

### Structural Patterns to Avoid

**Sentence uniformity:** AI clusters sentences at 15-25 words. Human writing mixes 5-word fragments with 30+ word constructions. Vary deliberately.

**Parallel construction overuse:** AI loves matching structures ("X enables Y. Z facilitates W. A drives B."). Break the pattern.

**Excessive hedging:** "It could be argued that..." / "To some extent..." / "Generally speaking..." — pick a position.

**Missing contractions:** AI avoids "don't", "won't", "it's", "that's". Humans use them constantly in informal writing.

**Passive voice clustering:** "It was determined that..." / "The system is configured to..." — use active voice by default.

**Present participial overuse:** "The system analyzes data, revealing key insights" — this construction appears 2-5x more in AI text.

### Platform-Specific Norms

#### Twitter/X (2026)
- Grok monitors tone: positive/constructive gets wider distribution
- Authenticity > polish: share real experiences including failures
- Threads get 63% higher engagement than single posts
- Soft CTAs ("DM me", "bookmark this") outperform hard sells
- Problem-Agitate-Solution framework works well

#### LinkedIn (2026)
- Hook must be under 200 characters (truncation point: ~210 chars)
- Never write paragraphs longer than 2-3 sentences
- Carousels: 24.42% engagement (4x higher than text)
- Personal journey/failure stories outperform generic business content
- Creator-led posts generate 3x more engagement than branded posts
- 54% of long-form LinkedIn posts are likely AI-generated — standing out means NOT sounding like them

#### GitHub PRs
- Use conventional commit prefixes: feat:, fix:, docs:, chore:, refactor:
- Imperative mood: "add support for X" not "Added support for X"
- AI PRs have 1.7x more defects, 3x readability issues, 75% more logic errors
- Explain WHY not just WHAT — AI describes changes without motivation
- Maintainers are actively restricting AI-generated PRs
- Missing context is the biggest tell: perfect grammar + no "why" = AI

#### Commit Messages
- AI tells: overly descriptive, formulaic prefixes on trivial changes, perfect grammar, no informal language
- Human tells: typos occasionally, context about why, references to conversations/decisions

### Humanization Techniques

**The 3-Minute Human Check:**
1. Would you say this aloud to a colleague?
2. Does it include at least one specific example or anecdote?
3. Have you avoided jargon that adds no meaning?

**Before/After Examples:**

AI: "In the modern era, technological advancements have revolutionized various industries, enhancing efficiency and productivity across the board."
Human: "Tech has changed everything about how we work — mostly for the better, sometimes not."

AI: "It is essential to know your audience."
Human: "You ever try writing without knowing who you're talking to?"

AI: "Utilization of these mechanisms facilitates optimization."
Human: "This approach makes workflows easier and faster."

### Writing Principles (Summary)

1. **Use short words over long ones** — "use" not "utilize", "help" not "facilitate"
2. **Use contractions** — "don't" not "do not", "it's" not "it is"
3. **Vary sentence length** — mix 5-word punches with longer explanations
4. **Be specific** — "loads 3x faster" not "significantly improves performance"
5. **Have opinions** — "X is better because..." not "It could be argued that X may offer certain advantages"
6. **Include personality** — reactions, asides, real experiences
7. **Break patterns** — if three sentences start the same way, rewrite one
8. **Active voice by default** — "We fixed the bug" not "The bug was fixed"
9. **Skip the throat-clearing** — delete "It's important to note that" and start with the actual point
10. **Read it aloud** — if it sounds like a press release, rewrite it

## Source Conflicts
- Some sources claim "delve" frequency dropped sharply in 2025 after becoming widely recognized, suggesting banned word lists need regular updates
- Detection tool false positive rates range 5-15% depending on tool and text type
- Model-specific tells (Claude vs GPT vs Gemini) are poorly documented — most lists aggregate across all models

## Currency Assessment
- Most recent sources: January-February 2026
- Topic velocity: Fast-moving (AI models adapt, tells evolve)
- Confidence in currency: High for patterns, Medium for specific word lists (evolving)

## Key Sources
- GPTZero: Most Common AI Vocabulary (2025-2026) — quantified frequency analysis
- Stanford: Scientists Using AI to Help Write Papers (2025) — academic markers
- Frontiers in Education: Lexical diversity analysis (2025) — linguistic metrics
- Tenorshare: 140+ Common AI Words (2026) — comprehensive word list
- Microsoft: Six Obvious AI Words (2025) — accessible overview
- Google Developer Documentation Style Guide — voice/tone authority
- CodeRabbit: AI-Assisted PR Quality Report (2025) — GitHub-specific metrics
- Conturae: 70+ AI-Only Words (2025) — categorized by usage pattern
- Multiple platform guides for Twitter/X and LinkedIn (2026)
