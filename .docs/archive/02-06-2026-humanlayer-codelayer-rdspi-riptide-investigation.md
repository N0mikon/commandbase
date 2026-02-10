---
date: 2026-02-06
status: archived
topic: "HumanLayer CodeLayer RDSPI Riptide Investigation"
tags: [research, humanlayer, codelayer, rpi, rdspi, riptide, workflow]
git_commit: 8e92bba
archived: 2026-02-09
archive_reason: "Informational-only research with no local code references. Finding (no public RDSPI evidence) is final. No relevance to ongoing work."
---

# HumanLayer CodeLayer RDSPI "Riptide" Investigation

## Research Question
Is HumanLayer/CodeLayer upgrading from RPI (Research Plan Implement) to RDSPI (Research Design Structure Plan Implement), codenamed "riptide"?

## Summary
No public evidence of RDSPI exists. All public sources consistently reference the three-phase RPI (Research, Plan, Implement) workflow. "Riptide" appears only as the name of a Claude Code plugin (`humanlayer/riptide-rpi`) that implements standard RPI for Linear tickets. If RDSPI is real, it's either internal/unreleased or in very early discussion stages with no public footprint.

## Detailed Findings

### What Exists Publicly: RPI Workflow
**Sources:** [ACE Guide](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md), [DeepWiki](https://deepwiki.com/humanlayer/advanced-context-engineering-for-coding-agents/3-the-research-plan-implement-workflow)

The RPI workflow is HumanLayer's established methodology, presented at AI Engineer Code Summit (Nov 2025) and documented in their Advanced Context Engineering guide:
- **Research**: Parallel sub-agents scan codebase, produce ~200 lines of compacted findings
- **Plan**: Reasoning model or human creates atomic, testable tasks with FACTS validation
- **Implement**: Fresh context executes plan with verification between steps
- Key principle: "Frequent Intentional Compaction" — reset context to 10-15% between phases, keep active work at 40-60%

### The "Riptide" Name
**Sources:** [humanlayer/riptide-rpi](https://github.com/humanlayer/riptide-rpi)

"Riptide" is the name of a Claude Code plugin, not a workflow evolution:
- Repository: `humanlayer/riptide-rpi` (created Dec 29, 2025, 4 stars, 7 commits)
- Description: "Research-Plan-Implement workflow for Linear tickets with Claude Code"
- Standard three-phase RPI — no Design or Structure phases mentioned
- Installation: `/plugin marketplace add humanlayer/riptide-rpi`

### CodeLayer Product
**Sources:** [humanlayer.dev](https://www.humanlayer.dev/), [GitHub](https://github.com/humanlayer/humanlayer)

CodeLayer is HumanLayer's open-source IDE for orchestrating AI coding agents:
- Built on Claude Code, 9.2k GitHub stars
- Features: MultiClaude parallel sessions, keyboard-first workflows, worktree support
- Active nightly builds (latest: codelayer-0.1.0-nightly-20260206)
- Uses RPI as core methodology — no RDSPI references in codebase or docs

### Community RPI Implementations
**Sources:** [patrob/rpi-strategy](https://github.com/patrob/rpi-strategy), [alexkurkin.com](https://www.alexkurkin.com/guides/claude-code-framework), [Block/Goose](https://block.github.io/goose/docs/tutorials/rpi/)

RPI has been widely adopted beyond HumanLayer:
- Block's Goose agent framework integrates RPI
- Multiple community implementations (brilliantconsultingdev, patrob)
- Alex Kurkin's framework adds a 4th Validation phase
- Patrick Robinson formalized FAR/FACTS validation scales
- None of these extensions use the RDSPI acronym

### The "Dumb Zone" Concept
**Sources:** [X/Twitter @nibzard](https://x.com/nibzard/status/1992314325638299879), [fanpino.com](https://fanpino.com/en/blog/context-engineering-rpi-workflow-ai-coding/)

Related concept from Dex Horthy: when >40% of context window is noise, model performance drops significantly. RPI combats this through aggressive compaction between phases. This theory could motivate adding Design and Structure phases as additional compaction points, but no public discussion of this exists.

## Source Conflicts
No conflicts — all sources consistently describe RPI as three phases. No source mentions RDSPI.

## Currency Assessment
- Most recent source: Nightly builds from Feb 6, 2026
- Topic velocity: Fast-moving (active development, daily builds)
- Confidence in currency: High — searched official repos, social media, community forums

## Assessment
The RDSPI concept with "riptide" codename has no public footprint. Most likely explanations:
1. **Internal/unreleased** — may exist in private repos, Slack, or internal planning docs
2. **Early discussion** — may have been mentioned in a live stream, podcast, or Discord that isn't indexed
3. **Misattribution** — the concepts of Design and Structure may come from a different source or community member's proposal
4. **Future announcement** — given daily nightly builds, new features ship frequently and may not be pre-announced

## Open Questions
- Was RDSPI mentioned in a specific podcast, livestream, or Discord conversation?
- Could the source be a community member's proposal rather than official HumanLayer?
- Is there a private CodeLayer Discord or Slack where workflow evolution is discussed?
