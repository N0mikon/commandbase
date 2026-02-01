# Verification Workflow Reference

Detailed verification procedures for plan implementation.

## The Gate Function

```
BEFORE marking any phase complete or updating checkboxes:

1. IDENTIFY: What commands verify this phase's success criteria?
2. RUN: Execute each command (fresh, complete - not cached)
3. READ: Full output - exit codes, pass/fail counts, error messages
4. VERIFY: Does output confirm ALL phase requirements?
   - If NO: State what failed, fix before continuing
   - If YES: State completion WITH evidence (command + output summary)
5. ONLY THEN: Update the checkbox in the plan file

Skip any step = false completion claim
```

## Evidence Format

When completing a phase, show evidence:
```
Phase 1 complete.

Verification:
- `npm test`: 47/47 passing, exit 0
- `npm run typecheck`: no errors, exit 0
- `npm run lint`: 0 warnings, exit 0

✓ All success criteria met. Proceeding to Phase 2...
```

**Not acceptable:**
- "Tests should pass now"
- "I've implemented the changes"
- "Phase complete" (without evidence)

## Verification Approach

After implementing each phase, follow the Gate Function:

1. **IDENTIFY** the verification commands from the plan's success criteria
2. **RUN** each command fresh (don't trust cached results)
3. **READ** full output:
   - Exit codes (0 = success)
   - Pass/fail counts
   - Error messages or warnings
4. **VERIFY** all criteria are met
5. **SHOW EVIDENCE** in your response before updating checkboxes

If any check fails:
- Do NOT update checkboxes
- Do NOT proceed to next phase
- Debug and fix the issue
- Re-run ALL verification commands
- Only then continue

## Common Verification Commands

| Project Type | Test Command | Typecheck | Lint |
|--------------|--------------|-----------|------|
| Node/TS | `npm test` | `npm run typecheck` | `npm run lint` |
| Python | `pytest` | `mypy .` | `ruff check .` |
| Rust | `cargo test` | `cargo check` | `cargo clippy` |
| Go | `go test ./...` | (built-in) | `golangci-lint run` |
