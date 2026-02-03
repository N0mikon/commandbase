---
name: debating-options
description: "Use this skill when the user says '/debating-options', 'debate these options', 'compare these choices', 'which should I choose', or wants parallel research on multiple options with synthesized recommendations. Launches research agents for each option, then synthesizes into a decision matrix. Default is objective analysis; use advocate mode when user is unsure or wants deeper exploration."
---

# Debating Options

Launch parallel research agents to investigate multiple options, then synthesize findings into a decision matrix with recommendation.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO SYNTHESIS WITHOUT COMPLETE RESEARCH FROM ALL AGENTS
```

If any research agent hasn't completed, you cannot synthesize findings or make recommendations.

**No exceptions:**
- Don't synthesize with partial results - wait for ALL agents
- Don't skip the judge synthesis step
- Don't present findings without the decision matrix
- Don't recommend without showing tradeoffs

## The Gate Function

```
BEFORE presenting any recommendation:

1. IDENTIFY: Extract 2-4 distinct options from user input
2. CLARIFY: If options unclear, ask user to specify
3. SPAWN: Launch one research agent per option (parallel)
4. WAIT: All agents must complete before proceeding
5. SYNTHESIZE: Run judge agent to create decision matrix
6. ONLY THEN: Present findings with recommendation

Skip any step = incomplete analysis
```

## When This Activates

- User invokes `/debating-options`
- User says "debate these options" or "compare these choices"
- User presents options and asks "which should I choose?"
- User wants deep comparative analysis, not a quick answer

## Modes

| Mode | Default | When to Use |
|------|---------|-------------|
| **Objective** | Yes | User wants facts and tradeoffs to decide themselves |
| **Advocate** | No | User is unsure, wants persuasive cases to help clarify thinking |

## The Process (Objective Mode - Default)

```
1. IDENTIFY OPTIONS
   - Extract 2-4 distinct options from context
   - If unclear, ask user to clarify the options

2. LAUNCH RESEARCHERS (parallel)
   - One background agent per option
   - Each agent researches their option objectively
   - Reports facts, tradeoffs, use cases without advocacy
   - No persuasion, just honest analysis

3. WAIT FOR RESULTS
   - Collect all research findings
   - Ensure all agents complete before synthesis

4. SYNTHESIZE (judge agent)
   - Create decision matrix with 5-6 criteria
   - Rate each option per criterion
   - Summarize core trade-offs
   - Provide recommendation with reasoning

5. PRESENT TO USER
   - Show decision matrix
   - Show synthesis and recommendation
   - User decides based on facts
```

## The Process (Advocate Mode - When Unsure)

Use when user says "I'm not sure", "help me decide", or requests advocate mode.

```
1. IDENTIFY OPTIONS (same as above)

2. LAUNCH ADVOCATES (parallel)
   - One background agent per option
   - Each agent argues FOR their assigned option
   - Persuasive but honest - finds genuine strengths
   - Acknowledges 1-2 weaknesses as trade-offs

3. WAIT FOR RESULTS (same as above)

4. SYNTHESIZE (judge agent)
   - Weighs advocate arguments
   - Creates decision matrix from competing cases
   - Declares winner with reasoning

5. PRESENT TO USER
   - Show each advocate's case
   - Show decision matrix
   - Show judge's recommendation
```

## Agent Prompts

### Objective Researcher Template (Default)

```
You are a RESEARCHER analyzing this option:

**Option:** [OPTION]

**Context:** [BACKGROUND IF RELEVANT]

Your job is to research this option objectively. Report facts, not advocacy.

Cover:
- What is this option? (brief description)
- Key strengths (factual, not persuasive)
- Key weaknesses (honest limitations)
- Best use cases (when this option fits)
- Poor use cases (when to avoid)

Format:
## [OPTION]

### Overview
[1-2 sentences]

### Strengths
- [factual bullet points]

### Weaknesses
- [honest limitations]

### Best For
- [use cases where this excels]

### Avoid When
- [situations where this is wrong choice]
```

### Advocate Agent Template (When Unsure)

```
You are an ADVOCATE for this position:

**Your Position:** [OPTION]

**Context:** [BACKGROUND IF RELEVANT]

Your job is to argue FOR this position. Be persuasive but honest.

Consider:
- When would this option be most valuable?
- What problems does it solve?
- What are the genuine strengths?

Also acknowledge 1-2 weaknesses (intellectual honesty), framed as manageable trade-offs.

Format:
## Argument for "[OPTION]"
[Your persuasive case - 150 words max]

### Key Strengths
- [bullet points]

### Acknowledged Trade-offs
- [1-2 honest weaknesses]
```

### Judge/Synthesizer Template

```
You are the JUDGE synthesizing research findings into a recommendation.

## Research Findings
[PASTE ALL AGENT OUTPUTS]

---

Create your synthesis in this exact format:

## Decision Matrix

| Criteria | [Option 1] | [Option 2] | [Option 3] |
|----------|------------|------------|------------|
| [criterion] | [rating + note] | [rating + note] | [rating + note] |

Include 5-6 meaningful criteria relevant to the decision domain.
Use ratings: Strong, Moderate, Weak

## Synthesis
[2-3 sentences on core trade-offs]

## Recommendation
**Winner: [Option]**
[3-4 sentences explaining why]
```

## Implementation Notes

- Use `subagent_type: general-purpose` for all agents
- Use `model: haiku` for researchers/advocates (fast, parallel)
- Use `model: sonnet` for judge (synthesis quality matters)
- Set `run_in_background: true` for parallel execution
- Use `TaskOutput` to collect results before judging

## Example Invocations

**Objective (default):**
```
User: /debating-options React vs Vue vs Svelte for my new project
```
Response: Launches 3 objective researchers, synthesizes into matrix.

**Advocate (when unsure):**
```
User: /debating-options I'm not sure whether to use REST or GraphQL
User: /debating-options --advocate Kubernetes vs Docker Swarm
```
Response: Launches advocates who argue for each option, judge decides.

## Mode Selection Logic

- Default to **Objective** mode
- Switch to **Advocate** mode if user:
  - Says "I'm not sure", "help me decide", "I can't choose"
  - Explicitly requests advocate mode
  - Seems paralyzed by the decision
  - Wants to understand *why* each option matters, not just facts

## Red Flags - STOP and Verify

If you notice any of these, pause:

- Synthesizing before all research agents complete
- Presenting recommendation without decision matrix
- Skipping the judge synthesis step
- Not showing tradeoffs for each option
- Defaulting to advocate mode without user indication

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "One agent is taking too long" | Wait. Partial research = partial recommendation. |
| "The answer is obvious" | Run the full process. Obvious answers may have hidden tradeoffs. |
| "User seems impatient" | Quality matters more than speed. Complete the analysis. |
| "I can synthesize as results come in" | Wait for ALL results. Order effects bias synthesis. |

## The Bottom Line

**No recommendation without complete research from all options.**

Identify options. Spawn parallel agents. Wait for all results. Synthesize with decision matrix. THEN recommend.

This is non-negotiable. Every debate. Every time.
