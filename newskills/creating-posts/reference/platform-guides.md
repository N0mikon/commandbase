# Platform Guides Reference

Per-platform voice, format constraints, character limits, and examples. Read this for the selected platform BEFORE drafting.

## Reddit

**Voice:** Casual, self-deprecating, honest about limitations. Talk like you're explaining your project to a friend at a meetup — not pitching to investors.

**Format:**
- Title: 300 characters max
- Self-post body: 40,000 characters max (but shorter is better)
- Markdown supported (bold, italic, links, code blocks)
- Flair often required — check subreddit rules

**Subreddit Norms:**

| Subreddit | Tone | What works | What doesn't |
|-----------|------|-----------|--------------|
| r/selfhosted | Practical, "here's what I run" | Setup details, screenshots, comparison to alternatives | Marketing speak, vague feature lists |
| r/sideproject | Honest journey, lessons learned | What went wrong, pivots, metrics | "Launching my startup" energy |
| r/webdev | Technical, show the code | Architecture decisions, performance numbers | "Check out my app" without substance |
| r/programming | Deep technical, opinionated | Novel approach, interesting problem, trade-offs | Tutorial-style, beginner-level |

**Good Reddit Posts:**

```
Title: I built a CLI tool that backs up my Docker volumes because I got tired of writing bash scripts at 2am

Body: Every time I set up a new container I'd write the same janky backup script.
After the third time rsync ate my Postgres data I figured I should just build
something proper.

It handles volume snapshots, rotation, and restore. Written in Go because I
wanted a single binary I could scp to any box.

What it does:
- Snapshots running volumes without stopping containers
- Configurable retention (I keep 7 daily, 4 weekly)
- Restore to any point with one command

What it doesn't do yet:
- Remote backup targets (it's local-only for now)
- Encryption at rest

Source: [link]

Happy to answer questions about the approach. Roast my code.
```

```
Title: Show r/selfhosted: replaced 4 SaaS subscriptions with one self-hosted stack

Body: Got tired of paying $47/month for tools I barely use. Spent a weekend
setting up [tool] + [tool] + [tool] behind Traefik.

Total cost: $5/month on a used Dell Optiplex.
Total setup time: about 6 hours (would be 2 if I hadn't fat-fingered my DNS records).

The good: everything works, I own my data, no more random price hikes.
The bad: I'm now the sysadmin and the support team.

Docker compose if anyone wants it: [link]
```

**Anti-Patterns for Reddit:**
- "I'm excited to share..." (instant downvote magnet)
- Feature bullet lists without context
- Not disclosing limitations
- Treating it like a product launch instead of a conversation

## Twitter/X

**Voice:** Punchy, hot take energy, conversational. Lead with the interesting part. No preamble.

**Format:**
- 280 characters per tweet (Premium: 25,000 for long-form)
- Links consume ~23 characters (t.co wrapping)
- Plain text only — no markdown
- 4 images, 1 video, or 1 GIF per tweet

**Thread Structure:**
1. Hook tweet — the thing that makes someone stop scrolling (280 chars)
2. Detail tweets — 2-5 tweets expanding on the hook (280 chars each)
3. CTA tweet — soft ask: "link in bio", "DM me", "bookmark this" (280 chars)

Threads get 63% higher engagement than single tweets. Soft CTAs outperform hard sells.

**Good Twitter/X Posts:**

Single tweet:
```
I replaced 4 SaaS tools with one Docker compose file.

Monthly cost went from $47 to $5.

Setup took 6 hours. Would do it again.
```

Thread:
```
Tweet 1: Built a CLI that backs up Docker volumes without stopping containers.

Here's why I couldn't just use rsync (thread)

Tweet 2: The problem: rsync on a running Postgres volume is a coin flip. Sometimes you get a clean backup. Sometimes you get corrupted pages.

Tweet 3: The fix: filesystem snapshots at the volume driver level. No container downtime. Consistent state guaranteed.

Tweet 4: It's ~2k lines of Go. Single binary, zero dependencies on the target machine.

Link: [url]
```

**Anti-Patterns for Twitter/X:**
- Starting with "I'm thrilled to announce..."
- Walls of text in a single tweet
- Hashtag spam (#coding #dev #programming #buildinpublic #tech)
- "Let me know what you think!" as the entire CTA

## Hacker News

**Voice:** Technical, understated, substance over marketing. HN readers can smell hype from orbit. Understate, don't oversell.

**Format:**
- Title: ~80 characters practical limit
- "Show HN:" prefix required for project showcases
- Body: plain text only, no markdown, no images
- URLs auto-linked
- Technical substance is the price of admission

**Good HN Posts:**

```
Title: Show HN: Volsnap - Docker volume backups without container downtime

Body: I kept losing data backing up running Postgres containers with rsync.
Built a tool that uses filesystem-level snapshots instead.

- Go, single binary, no runtime deps
- Handles snapshot, rotation, restore
- Works with any volume driver that supports snapshots

Limitations: local targets only (no S3/remote yet), Linux-only, needs
volume driver snapshot support.

Tested against Postgres, MariaDB, and Redis. Postgres was the motivation --
rsync on a live WAL directory is asking for trouble.

Code: [link]
```

```
Title: Show HN: I replaced 4 SaaS tools with self-hosted alternatives

Body: After a price hike on one of my tools I spent a weekend migrating
to self-hosted equivalents. Wrote up the experience including what broke.

The stack: [tool1] for X, [tool2] for Y, [tool3] for Z, all behind Traefik.

What went well: data migration was straightforward, performance is better.
What didn't: SMTP setup took 3 hours of debugging SPF records.

Not a general recommendation -- this makes sense if you already run a homelab.

Writeup: [link]
```

**Anti-Patterns for HN:**
- Marketing language of any kind ("revolutionary", "game-changing")
- Vague feature descriptions without technical detail
- Not mentioning limitations or trade-offs
- Asking for upvotes or engagement
- "In today's world..." style openings

## LinkedIn

**Voice:** Professional but not corporate. Results-focused. Personal experiences outperform generic business content. The first ~200 characters are the hook — they must stand alone because everything after gets truncated behind "...see more".

**Format:**
- Post: 3,000 characters max
- First ~200 characters = hook (before truncation)
- Markdown NOT supported (use line breaks for structure)
- Hashtags: 3-5 recommended
- Short paragraphs (2-3 sentences max)

**Good LinkedIn Posts:**

```
I spent $47/month on 4 SaaS tools I barely used.

Last weekend I replaced them all with self-hosted alternatives
running on a $50 used Dell Optiplex.

Setup took 6 hours. Monthly cost is now $5.

The catch: I'm now the sysadmin. When something breaks at 11pm
that's on me.

Worth it? For my use case, absolutely. I own my data, I control
the updates, and I stopped worrying about surprise price hikes.

Not for everyone -- you need to enjoy tinkering with servers.
But if you're already running a homelab, the ROI is immediate.

#selfhosted #homelab #devtools
```

```
Most side projects fail because people build features nobody asked for.

Mine almost did too.

I spent 3 months building a Docker backup tool. The first version
had a web dashboard, email alerts, and Slack integration.

Nobody used any of that.

What people actually wanted: a single command that backs up their
volumes without stopping containers.

So I deleted 60% of the code and shipped a CLI.

Downloads went from 12/month to 400+.

Lesson: the feature you're most proud of is probably the one
to cut first.

#buildinpublic #devtools #lessons
```

**Anti-Patterns for LinkedIn:**
- Corporate buzzwords ("synergy", "paradigm shift", "thought leader")
- Starting with a question nobody was asking ("Ever struggled with...?")
- Emoji-heavy formatting
- Long paragraphs (instant scroll-past)
- Generic advice without personal experience

## Discord

**Voice:** Conversational, community-oriented. You're talking to people who share your interests, not an audience. Keep it short — Discord messages that need scrolling get skipped.

**Format:**
- Message: 2,000 characters max
- Markdown supported (bold, italic, code blocks, spoilers)
- Server/channel context matters — match the room's energy
- Embeds: 6,000 characters total (rarely needed for posts)

**Good Discord Posts:**

```
hey all - built a CLI tool for backing up Docker volumes without
stopping containers. been using it on my homelab for a few weeks
and it hasn't eaten any data yet (famous last words)

handles postgres, mariadb, redis - basically anything with a
volume driver that supports snapshots.

single Go binary, no deps. `volsnap backup` and you're done.

repo: [link]

would love feedback if anyone tries it. especially around the
retention policy config -- not sure if the YAML format is intuitive.
```

```
just migrated off [SaaS tool] to self-hosted [alternative]. took about
2 hours including the data export/import.

the only annoying part was getting SMTP working for notifications.
if anyone's done this and has a working postfix config, I'd love
to compare notes.

running it behind traefik on a mini PC. so far so good.
```

**Anti-Patterns for Discord:**
- Formal language that doesn't match the channel
- Long-form essays (save those for Reddit/HN)
- Tagging @everyone for a project share
- Not reading the room — some channels are help-only, not showcase
