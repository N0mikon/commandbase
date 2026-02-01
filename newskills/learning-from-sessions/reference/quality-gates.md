# Quality Gates

Every extracted skill must pass these gates before being saved. These prevent skill sprawl, vague knowledge, and unverified solutions.

## Worth Assessment

Before extracting, confirm the discovery passes at least 3 of these 4 criteria:

1. **Recurrence**: Will this problem appear again? In this project or others?
2. **Non-triviality**: Was the solution non-obvious? Did it require investigation?
3. **Transferability**: Does the knowledge apply beyond this exact situation?
4. **Time savings**: Would having this skill save meaningful time in a future session?

**Not worth extracting:**
- Simple typos or syntax errors
- One-time issues (specific outage, corrupted file)
- Project-specific configuration better suited for CLAUDE.md or handover docs
- Trivial fixes found within seconds
- Knowledge that's clearly documented in official docs (link to docs instead)

When a discovery fails the worth assessment:
```
I reviewed the session discovery but it doesn't meet the extraction threshold:
- [Which criteria it failed and why]

This is better captured as: [alternative -- CLAUDE.md entry, handover note, or nothing]
```

## Pre-Save Checklist

Run every item before writing the skill file:

### Content Quality
- [ ] Description contains specific trigger conditions (error messages, framework names, situations)
- [ ] Solution has been verified to work in this session
- [ ] Content is specific enough to be actionable (not "check the configuration")
- [ ] Content is general enough to be reusable (not tied to one filename or path)
- [ ] No sensitive information (credentials, internal URLs, API keys, private paths)
- [ ] Doesn't duplicate an existing skill or official documentation
- [ ] Web research conducted when the topic involves specific technology

### Structure
- [ ] Frontmatter has `name` and `description` fields
- [ ] Name matches `^[a-z0-9-]+$`, no leading/trailing/consecutive hyphens, max 64 chars
- [ ] Description is under 1024 characters, no angle brackets
- [ ] Uses the extracted-skill-template.md format
- [ ] Each solution step is independently verifiable

### Scope
- [ ] Saved to correct location (project vs user-level)
- [ ] Cross-linked with related skills if applicable
- [ ] Version and date included

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

## When NOT to Extract

Some valuable session knowledge doesn't belong in a skill file:

| Knowledge Type | Better Home |
|---------------|-------------|
| Project coding conventions | CLAUDE.md (project root) |
| Team workflow preferences | CLAUDE.md (project root) |
| One-time setup instructions | Handover document |
| Session-specific context | Handover document |
| Correction to Claude behavior | CLAUDE.md entry |
| Simple preference ("always use X not Y") | CLAUDE.md entry |

## Output Decision Flow

```
Is the knowledge reusable across projects?
├── YES: Is it multi-step with clear trigger conditions?
│   ├── YES → New skill file (~/.claude/skills/)
│   └── NO → CLAUDE.md entry (~/.claude/CLAUDE.md)
└── NO: Is it specific to this project?
    ├── YES: Is it a behavioral correction?
    │   ├── YES → CLAUDE.md entry (./CLAUDE.md)
    │   └── NO → Handover document or project CLAUDE.md
    └── NO → Probably not worth saving
```
