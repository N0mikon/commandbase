---
name: linting-vault
description: "Use this skill when checking vault health, validating note quality, or running vault-wide linting checks. This includes detecting broken wikilinks, validating frontmatter against schema, finding orphaned notes with no incoming links, checking heading structure, identifying empty files, and generating actionable health reports. Activate when the user says 'lint vault', 'check vault health', 'find broken links', 'validate frontmatter', or 'run vault checks'."
---

# Linting Vault

You are running health checks on an Obsidian vault. This skill validates note quality, link integrity, frontmatter correctness, and structural consistency. It activates standalone (on-demand vault health checks) or is delegated to by `/implementing-vault` for post-phase verification.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO LINT REPORT WITHOUT READING VAULT CLAUDE.MD FIRST
```

The vault CLAUDE.md defines frontmatter schema, tag taxonomy, folder conventions, and naming rules. Without reading it, you cannot validate anything — you don't know what "correct" looks like.

**No exceptions:**
- Don't lint frontmatter without knowing the required properties
- Don't check tag consistency without knowing the taxonomy
- Don't report orphans without understanding the vault's MOC structure
- Don't assume conventions — read them from CLAUDE.md

## The Gate Function

```
BEFORE producing any lint report:

1. READ: Vault CLAUDE.md for vault path, frontmatter schema, tag taxonomy, conventions
2. SCOPE: Determine target — specific notes (Mode A) or full vault (Mode B)
3. INVENTORY: Count notes in scope, identify file types
4. EXECUTE: Run lint checks from ./reference/lint-checks.md
5. REPORT: Present findings with actionable fix suggestions
6. ONLY THEN: Offer to save report if user wants persistence

Skip CLAUDE.md read = wrong validation rules = useless report
```

## Initial Response

When invoked, first determine the mode:

**If specific notes or a folder is provided:**
```
Running targeted lint on [N] notes...
[Read vault CLAUDE.md for conventions]
[Execute Mode A checks]
```

**If no argument or "full lint" requested:**
```
Running full vault lint...
[Read vault CLAUDE.md for conventions]
[Execute Mode B checks — this may take a moment for large vaults]
```

**If invoked by /implementing-vault:**
```
Running post-phase lint on affected notes...
[Execute Mode A checks on the specified notes]
```

## Modes

### Mode A: Targeted Lint

Use this mode after specific operations or when the user points to particular notes/folders.

**Steps:**
1. Read vault CLAUDE.md for conventions
2. Identify target notes (from argument, or notes affected by a recent operation)
3. Run checks: broken wikilinks, frontmatter validation, heading structure
4. If notes were moved: also run orphan detection
5. Present targeted report

See ./reference/lint-checks.md "Mode A: Targeted Lint" for check procedures and report format.

### Mode B: Full Vault Lint

Use this mode for comprehensive health assessment of the entire vault.

**Steps:**
1. Read vault CLAUDE.md for conventions
2. Inventory all .md files in the vault
3. Run all 7 checks in phases (structure → links → metadata)
4. Compute health score
5. Present full health report with findings grouped by severity

See ./reference/lint-checks.md "Mode B: Full Vault Lint" for phases, procedures, and health thresholds.

## Lint Checks

Seven checks available, detailed in ./reference/lint-checks.md:

1. **Broken wikilinks** — verify `[[link]]` targets exist
2. **Frontmatter validation** — required properties, valid YAML, correct types
3. **Orphan detection** — notes with zero incoming links
4. **Heading structure** — no skipped heading levels
5. **Empty file detection** — notes with no body content
6. **Duplicate detection** — notes with identical normalized names
7. **Tag consistency** — tags match taxonomy, no case mismatches or typos

Format validation rules (wikilink syntax, callout types, frontmatter constraints) are in ./reference/ofm-validation-rules.md.

## Output Behavior

Present lint results directly in the response. After presenting:

```
Would you like me to save this report to .docs/vault-health/?
```

Only save if the user confirms. Don't auto-create files.

## Error Recovery

**Recoverable errors:**
- Vault CLAUDE.md not found: Ask user for vault path and conventions, proceed with defaults
- MCP not available: Fall back to filesystem tools (Glob, Grep, Read)
- Some notes unreadable: Skip and note in report, continue with remaining notes

**Blocking errors:**
- No vault path determinable: Cannot lint without knowing what to lint
- Vault directory doesn't exist: Cannot proceed

## Red Flags - STOP and Verify

If you notice any of these, pause:

- About to validate frontmatter without knowing the vault's schema
- Reporting tag inconsistencies without reading the tag taxonomy
- Running full vault lint without warning the user it may take time
- Making changes to notes during a lint run (linting is read-only)
- Claiming healthy without running all applicable checks

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Most vaults use standard frontmatter" | Read CLAUDE.md. Every vault defines its own schema. |
| "Full vault lint is overkill" | User asked for it. Run all checks. |
| "These orphans are probably intentional" | Report them. User decides what's intentional. |
| "Tag taxonomy is obvious" | Read it from CLAUDE.md. Obvious assumptions create false positives. |
| "I'll fix issues as I find them" | Linting is read-only. Report, don't fix. User decides. |

## The Bottom Line

**Read conventions. Run checks. Report findings. Let the user decide what to fix.**

Linting is diagnostic, not therapeutic. Your job is to surface issues with evidence, not to silently fix things. This is non-negotiable. Every lint run. Every time.
