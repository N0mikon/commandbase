# Quality Gates

Every learnings document must pass these gates before being saved. These prevent learnings sprawl, vague knowledge, and unverified discoveries.

## Worth Assessment

Before extracting, confirm the discovery passes at least 3 of these 4 criteria:

1. **Recurrence**: Will this problem appear again? In this project or others?
2. **Non-triviality**: Was the solution non-obvious? Did it require investigation?
3. **Transferability**: Does the knowledge apply beyond this exact situation?
4. **Time savings**: Would having this skill save meaningful time in a future session?

**Not worth capturing:**
- Simple typos or syntax errors
- One-time issues (specific outage, corrupted file)
- Trivial fixes found within seconds
- Knowledge that's clearly documented in official docs (link to docs instead)

When a discovery fails the worth assessment:
```
I reviewed the session discovery but it doesn't meet the capture threshold:
- [Which criteria it failed and why]

Not worth documenting in .docs/learnings/.
```

## Pre-Save Checklist

Run every item before writing the learnings document:

### Content Quality
- [ ] Each discovery was verified during this session
- [ ] Content is specific enough to be actionable (not "check the configuration")
- [ ] No sensitive information (credentials, internal URLs, API keys, private paths)
- [ ] Doesn't duplicate existing learnings or skills
- [ ] Session error context included when errors.log exists

### Structure
- [ ] Uses the learnings template format (Error Summary, Discoveries, Debug References, Deferred Actions)
- [ ] Error Summary omitted when no session or no errors (not left empty)
- [ ] Debug References omitted when no debug files found (not left empty)
- [ ] Each deferred action names a specific skill, CLAUDE.md section, or pattern

### Deferred Actions
- [ ] Every deferred action is concrete (names the skill/entry to create)
- [ ] Actions are categorized: create skill, add to CLAUDE.md, or update existing skill
- [ ] No vague actions like "maybe create a skill" or "consider updating something"

## Anti-Patterns

These are the most common mistakes when extracting skills. Watch for them.

### Over-Extraction
**Symptom**: Extracting a skill from every minor fix.
**Why it's bad**: Floods skill directories with low-value content. Makes useful skills harder to find.
**Fix**: Apply the worth assessment strictly. When in doubt, don't extract.

### Vague Descriptions
**Symptom**: "Helps with React problems" or "Fixes deployment issues."
**Why it's bad**: Won't surface during semantic matching. Claude can't distinguish this from its general knowledge.
**Fix**: Include specific error messages, framework names, and exact trigger conditions. See description-optimization.md.

### Unverified Solutions
**Symptom**: Extracting a solution that "should work" but wasn't tested in this session.
**Why it's bad**: Spreads potentially wrong information. Worse than no skill at all.
**Fix**: Only extract solutions that were verified during the session. If partially verified, note the limitation.

### Documentation Duplication
**Symptom**: Skill content that restates official documentation.
**Why it's bad**: Adds nothing Claude doesn't already know. Goes stale when docs update.
**Fix**: Link to the documentation. Only extract what's missing from docs (the non-obvious part, the workaround, the gotcha).

### Stale Knowledge
**Symptom**: Skills referencing specific versions without noting version constraints.
**Why it's bad**: Solutions for v2.x may break on v3.x. Users hit confusing failures.
**Fix**: Include version constraints in trigger conditions. Add a date stamp. Note when behavior is version-dependent.

## Deferred Action Decision Flow

All learnings go to `.docs/learnings/`. The Deferred Actions checklist tells future sessions what to do:

```
Is the discovery reusable across projects?
├── YES: Is it multi-step with clear trigger conditions?
│   ├── YES → Deferred: Create skill (~/.claude/skills/)
│   └── NO → Deferred: Add to ~/.claude/CLAUDE.md
└── NO: Is it specific to this project?
    ├── YES → Deferred: Add to ./CLAUDE.md or update existing skill
    └── NO → Probably not worth capturing
```
