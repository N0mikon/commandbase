---
name: brainstorming-services
description: "Use this skill when exploring direction and preferences for homelab or Docker service infrastructure before deployment. This includes discussing reverse proxy choices (Traefik vs Nginx), compose architecture (single vs per-service), backup strategies (Borg vs restic), networking topology, and service dependency ordering."
---

# Brainstorming Services

You are exploring direction and preferences for homelab or Docker service infrastructure through adaptive questioning BEFORE writing any compose files or deploying anything. This skill activates when users want to brainstorm infrastructure architecture, discuss service stack choices, or settle deployment topology. It produces a `.docs/brainstorm/` artifact that captures stack decisions and dependency relationships.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
CAPTURE STACK DECISIONS BEFORE DEPLOYING
```

Infrastructure brainstorming settles service stack and topology BEFORE writing any compose files, Dockerfiles, or configuration. Deploying without settled direction leads to migration pain, networking headaches, and cascade failures.

**No exceptions:**
- Don't assume users want Traefik — Nginx Proxy Manager, Caddy, and others are valid
- Don't skip brainstorming because the stack is "simple" — even a single service has networking and backup decisions
- Don't recommend services before settling on constraints — requirements drive stack choices, not the reverse
- Don't ignore decision interdependencies — choosing a reverse proxy constrains auth options, which constrains networking

## The Gate Function

```
BEFORE generating questions:

1. IDENTIFY: What infrastructure goal is being brainstormed?
2. ASSESS: Which service domains are relevant? (stack, compose, networking, backup, dependencies)
3. MAP: Identify decision interdependencies between domains
4. ORDER: Arrange topics so prerequisite decisions come first
5. CONFIRM: User selects which topics to brainstorm
6. ONLY THEN: Begin 4-question rhythm per topic (in dependency order)

Skipping dependency mapping = decisions that contradict each other
```

## Initial Response

When invoked, determine the infrastructure goal:

### If infrastructure topic provided as argument:
1. Identify which service domains are relevant
2. Map decision interdependencies
3. Order topics by dependency chain
4. Present topics for selection

### If no argument provided:
```
I'll help you explore direction and preferences for your infrastructure.

What's the infrastructure goal? For example:
- New homelab stack from scratch
- Adding a service to existing infrastructure
- Reorganizing Docker compose setup
- Planning backup and recovery strategy
- Setting up remote access / reverse proxy

Describe what you want the infrastructure to do.
```

### After goal is identified:
```
Infrastructure Goal: [Goal from input]
Relevant Domains: [Which of the 5 service domains apply]
Decision Order: [Which decisions must come first due to dependencies]

Topics to explore (ordered by dependencies):

[ ] [Topic 1] - [What this settles] (prerequisite for Topic 3)
[ ] [Topic 2] - [What this settles]
[ ] [Topic 3] - [What this settles] (depends on Topic 1)
[ ] [Topic 4] - [What this settles]

Which topics should we cover?
```

Present topics using AskUserQuestion with `multiSelect: true`. NO "skip all" option — user invoked this command to brainstorm.

## Service Domains

See `reference/services-question-domains.md` for domain-specific question templates.

Unlike code brainstorming (which detects domain via action verbs), services brainstorming draws from 5 fixed domains with explicit interdependencies between them.

**Service Domains:**

| Domain | What It Settles | Constrains |
|--------|----------------|------------|
| Stack Selection | Which services to run, core tools | Compose, Networking |
| Compose Architecture | How services are organized in compose files | Dependencies |
| Networking | How services communicate and are accessed | Backup scope |
| Backup Strategy | What's backed up, how, and where | — |
| Dependencies & Ordering | Startup order, health checks, failure behavior | — |

**Decision Interdependency Map:**
- **Stack → Compose**: Choosing Traefik means labels-based routing which affects compose structure
- **Stack → Networking**: Choosing Cloudflare tunnels vs Tailscale determines networking topology
- **Compose → Dependencies**: Per-service compose files change how dependencies are managed
- **Networking → Backup**: VPN/tunnel choice affects which backup destinations are reachable

**Domain Selection Process:**
1. All 5 domains are potentially relevant
2. Identify which domains apply to this infrastructure goal
3. Map interdependencies between selected domains
4. Order topics so prerequisite decisions come before dependent ones
5. Present ordered topics for user selection

## Process

### Step 1: Topic Selection

Present 3-4 service-specific topics using AskUserQuestion with `multiSelect: true`.

**Topic Generation Guidelines:**
- Topics must be specific to THIS infrastructure goal, not generic
- Each topic should represent a real stack decision
- Show dependency relationships in topic descriptions
- Draw from `reference/services-question-domains.md`
- Order topics so prerequisite decisions come first

### Step 2: Deep Brainstorming

For each selected topic (in dependency order), use the 4-question rhythm:

1. Announce: "Let's explore [Topic]"
2. If this topic depends on a previous decision, reference it: "Since we chose [previous decision], here's how that affects [this topic]..."
3. Ask 4 questions using AskUserQuestion
   - 2-3 concrete options per question
   - Options reflect real infrastructure choices: "Traefik" not "Option A"
   - Include "You decide" option when reasonable
   - "Other" is added automatically by the tool
4. After 4 questions, check: "More questions about [topic], or move on?"
   - If "More" → ask 4 more, check again
   - If "Move on" → proceed to next topic

**Question Design:**
- Each answer can inform the next question (choosing Traefik → ask about labels vs file provider)
- Reference how earlier decisions constrain current options
- Questions probe direction, NOT configuration ("Traefik or Nginx?" not "which Traefik middleware?")
- If user picks "Other", capture input, reflect back, confirm understanding

### Step 3: Scope Guardrail

If user mentions something outside the infrastructure brainstorm scope:

```
"[Mentioned capability] sounds like it belongs in a separate brainstorm or implementation task.
I'll note it as a deferred idea so it's not lost.

Back to [current topic]: [return to current question]"
```

Track deferred ideas for inclusion in brainstorm artifact.

### Step 4: Brainstorm Artifact Creation

After all topics explored:

1. Confirm: "Ready to capture these decisions?"
2. Compile decision dependency chain showing which choices constrain which
3. Spawn a `docs-writer` agent via the Task tool:

   ```
   Task prompt:
     doc_type: "brainstorm"
     topic: "<infrastructure goal>"
     tags: [services]
     content: |
       <compiled brainstorm using ./templates/brainstorm-template.md>
   ```

4. Present summary and next steps

## Output Format

```
BRAINSTORM COMPLETE
===================

Brainstorm captured at: .docs/brainstorm/{topic-name}.md

Stack decisions settled:
- [Key stack choice 1]
- [Key stack choice 2]
- [Key stack choice 3]

Decision dependencies:
- [Choice A] → constrains → [Choice B]

Deferred ideas: [count or "None"]

Next steps:
- When Services BRDSPI is available: /researching-services to investigate implementation
- For now: Use these decisions to guide infrastructure setup manually
- Reference this brainstorm when writing compose files and configs
```

## Error Recovery

**Recoverable errors** (fix and continue):
- User unclear on infrastructure goal: Ask clarifying question about what they want the infrastructure to do
- Dependency conflict detected: Present the conflict, ask user to resolve by revisiting earlier decision

**Blocking errors** (stop and ask):
- No infrastructure goal identified: Cannot proceed without knowing what to build
- All topics declined: Ask if user wants different topics or to skip brainstorming

## Self-Improvement

Before finishing, review this skill execution:

- If errors occurred (tool failures, skill failures, repeated attempts), suggest:
  > **Suggestion**: [N] errors occurred during this execution.
  > Consider running `/extracting-patterns` to capture learnings.
  >
  > Errors: [brief summary of error types]
- Only suggest when errors are meaningful — use judgment about significance.
- Do not auto-run. Suggest only.

## Red Flags - STOP and Refocus

If you notice any of these, pause:

- Asking code-specific questions (API design, UI layout) — wrong domain
- Asking vault-specific questions (MOCs, Zettelkasten) — wrong domain
- Recommending specific Docker image versions or config syntax — that's implementation
- Ignoring decision interdependencies — decisions may contradict each other
- Generating generic questions not tailored to this infrastructure goal
- Not tracking deferred ideas
- Asking more than 4 questions before checking "More or move on?"
- Proceeding with dependent topics before their prerequisites are settled

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Everyone uses Traefik" | Many reverse proxies exist. Ask, don't assume. |
| "This stack is simple, skip brainstorming" | Simple stacks have networking and backup decisions. Capture them. |
| "I should suggest the most popular services" | Popularity != fit. Capture requirements first. |
| "Dependencies don't matter for small stacks" | Even 2-3 services have startup order and failure behavior. |
| "The user can restructure later" | Infrastructure migration is painful. Get direction right upfront. |

## The Bottom Line

**Brainstorming captures STACK DIRECTION, not SERVICE CONFIGURATION.**

The user knows what they want to run. Your job is to extract their infrastructure philosophy and stack preferences through concrete questions — not Docker image tags, not compose YAML syntax, not middleware config. Direction first, configuration later.

This is non-negotiable. Every stack. Every time.
