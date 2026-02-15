---
date: 2026-02-14
status: complete
topic: "HumanLayer Thoughts and Superpowers Attribution Research"
tags: [research, humanlayer, superpowers, attribution, readme]
git_commit: b37f5f6
---

# HumanLayer Thoughts and Superpowers Attribution Research

## Research Question
What exactly did commandbase borrow from HumanLayer's thoughts system and obra's Superpowers, for accurate README attribution?

## Summary
HumanLayer's thoughts system is a context management approach using a `thoughts/` directory, file:line references as documentation, handoffs instead of compacting, and an RPI (research-plan-implement) workflow. Superpowers provides iron gate enforcement patterns with mandatory steps, rationalization prevention, and deletion penalties for skipping workflow phases.

## Detailed Findings

### HumanLayer Thoughts System
**Sources:** https://github.com/humanlayer/humanlayer, https://humaineinterface.substack.com/p/i-mastered-the-claude-code-workflow

Core concepts:
- `thoughts/` directory for context management (shared/research/, shared/plans/, shared/handoffs/)
- Never exceed 60% context window utilization ("dumb zone" above 40-60%)
- File:line references instead of code snippets to prevent documentation drift
- Handoffs instead of compacting - structured markdown documents capture session state for next session
- RPI workflow: Research (parallel agents explore codebase), Plan (iterative with 5+ revisions), Implement (one phase at a time), Validate
- Specs as primary artifacts, not disposable conversation history

### obra's Superpowers
**Sources:** https://github.com/obra/superpowers, https://blog.fsck.com/2025/10/09/superpowers/

Core concepts:
- Iron Law pattern: "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST" with deletion enforcement
- Gate functions that block progression until requirements are met
- Rationalization prevention tables that anticipate and counter excuses for skipping steps
- Psychological enforcement using Cialdini's persuasion principles
- Pressure-tested skills validated against scenarios where Claude might skip steps
- Mandatory skill checking before any action ("even if there's only a 1% chance a skill applies")

### What commandbase borrowed
- From HumanLayer: `.docs/` system (adapted from `thoughts/`), RPI workflow (expanded to BRDSPI), handoff pattern, context management philosophy
- From Superpowers: Iron Law/gate function enforcement pattern, rationalization prevention tables, mandatory skill structure

## Sources
- https://github.com/humanlayer/humanlayer
- https://github.com/obra/superpowers
- https://humaineinterface.substack.com/p/i-mastered-the-claude-code-workflow
- https://blog.fsck.com/2025/10/09/superpowers/
- https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md
