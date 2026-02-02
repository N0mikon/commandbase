# Debug Session Template

Use this template for debug session files in `.docs/debug/{slug}.md`.

## File Naming

- **Location**: `.docs/debug/`
- **Format**: `{slug}.md` (lowercase, hyphens, max 30 chars)
- **Derived from**: First few words of issue description
- **Examples**: `login-fails-silently.md`, `api-returns-500.md`

## Template

```markdown
---
status: gathering | investigating | fixing | verifying | resolved
trigger: "[verbatim user input that started this session]"
created: [ISO timestamp]
updated: [ISO timestamp]
---

## Current Focus
<!-- OVERWRITE on each update - always reflects NOW -->

hypothesis: [current theory being tested]
test: [how testing it]
expecting: [what result means if true/false]
next_action: [immediate next step]

## Symptoms
<!-- Written during gathering, then IMMUTABLE -->

expected: [what should happen]
actual: [what actually happens]
errors: [error messages if any]
reproduction: [how to trigger]
started: [when it broke / always broken]

## Eliminated
<!-- APPEND only - prevents re-investigating after /clear -->

- hypothesis: [theory that was wrong]
  evidence: [what disproved it]
  timestamp: [when eliminated]

## Evidence
<!-- APPEND only - facts discovered during investigation -->

- timestamp: [when found]
  checked: [what was examined]
  found: [what was observed]
  implication: [what this means]

## Resolution
<!-- OVERWRITE as understanding evolves -->

root_cause: [empty until found]
fix: [empty until applied]
verification: [empty until verified]
files_changed: []
```

## Section Rules

| Section | Rule | Rationale |
|---------|------|-----------|
| Frontmatter.status | OVERWRITE | Reflects current phase |
| Frontmatter.trigger | IMMUTABLE | Original problem statement |
| Frontmatter.updated | OVERWRITE | Track last modification |
| Current Focus | OVERWRITE | Always reflects NOW |
| Symptoms | IMMUTABLE after gathering | Reference point for verification |
| Eliminated | APPEND only | Prevents re-investigation |
| Evidence | APPEND only | Builds case for root cause |
| Resolution | OVERWRITE | Evolves as understanding grows |

## Status Transitions

```
gathering -> investigating -> fixing -> verifying -> resolved
                  ^              |           |
                  |______________|___________|
                  (if verification fails)
```

## Resume Behavior

When reading debug file after `/clear`:

1. Parse frontmatter -> know status
2. Read Current Focus -> know exactly what was happening
3. Read Eliminated -> know what NOT to retry
4. Read Evidence -> know what's been learned
5. Continue from next_action

The file IS the debugging brain. Claude should resume perfectly from any interruption.

## Update Discipline

**CRITICAL:** Update the file BEFORE taking action, not after.

If context resets mid-action, the file shows what was about to happen, enabling seamless resume.

## Size Constraints

Keep debug files focused:
- Evidence entries: 1-2 lines each, just facts
- Eliminated: brief - hypothesis + why it failed
- No narrative prose - structured data only

If evidence grows large (10+ entries), check if you're going in circles. Review Eliminated section.

## Cleanup

After debug complete:
- Option 1: Delete file (if learnings extracted via `/learning-from-sessions`)
- Option 2: Keep for reference (if complex issue worth preserving)

No automatic archival - user decides.
