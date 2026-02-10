---
date: 2026-02-09
status: current
topic: reviewing-security skill analysis
tags: [security, skill-research, code-review, secrets-detection]
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Updated stale file paths (newskills -> plugins), expanded content to match current SKILL.md, added frontmatter"
references:
  - plugins/commandbase-git-workflow/skills/reviewing-security/SKILL.md
---

# Research: reviewing-security Skill

## Overview

The `reviewing-security` skill (`plugins/commandbase-git-workflow/skills/reviewing-security/SKILL.md`) reviews code for security vulnerabilities before committing to public repositories. It produces a verdict (PASS/WARN/BLOCK) based on severity of issues found.

**Plugin**: commandbase-git-workflow
**Allowed tools**: Read, Grep, Glob, LS, Bash, AskUserQuestion
**Trigger phrases**: `/review-security`, `security review`, `check for secrets`, `is this safe to commit publicly`

## The Iron Law

```
NO PUBLIC COMMIT WITH CRITICAL SECURITY ISSUES
```

If CRITICAL issues are found, the commit must be blocked. Secrets in public repos cannot be unlearned by the internet.

**No exceptions:**
- Don't approve code with hardcoded secrets
- Don't approve code with unvalidated user input in SQL/commands
- Don't approve code with credentials in plaintext
- Don't skip review because "it's just a small change"

## The Gate Function

The skill enforces a strict sequential process before issuing any verdict:

1. **SCOPE** -- Identify files to review (staged files or specified paths)
2. **SCAN** -- Run automated secret detection
3. **REVIEW** -- Manual inspection for each vulnerability category
4. **CLASSIFY** -- Categorize findings by severity
5. **VERDICT** -- PASS (no issues), WARN (medium only), or BLOCK (critical/high found)
6. **REPORT** -- Findings with remediation guidance

Skipping any step risks missed vulnerabilities.

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| **CRITICAL** | Immediate exploit risk, secrets exposed | BLOCK commit |
| **HIGH** | Serious vulnerability, likely exploitable | BLOCK commit |
| **MEDIUM** | Potential issue, context-dependent | WARN, recommend fix |
| **LOW** | Best practice violation, minor concern | Note for awareness |

## Review Modes

### Mode A: Full Review (Default for Public Repos)
Checks all categories:
1. Secrets and credentials
2. Injection vulnerabilities
3. Authentication/authorization
4. Data exposure
5. Dependency vulnerabilities
6. Code quality security

### Mode B: Quick Scan
Checks critical categories only:
1. Secrets and credentials
2. Obvious injection vulnerabilities

## Review Process (6 Steps)

### Step 1: Secret Detection
Scan for hardcoded secrets, API keys, and credentials.

**CRITICAL patterns:**
```regex
api[_-]?key\s*[:=]\s*['"][a-zA-Z0-9]{16,}
AKIA[0-9A-Z]{16}
-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----
password\s*[:=]\s*['"][^'"]+['"]
(bearer|token|auth)\s*[:=]\s*['"][a-zA-Z0-9\-_.]+['"]
(mongodb|postgresql|mysql|redis):\/\/[^:]+:[^@]+@
.env contents committed (not in .gitignore)
```

**HIGH patterns:**
- Hardcoded URLs with credentials
- Base64-encoded strings that decode to secrets
- Comments containing "password", "secret", "key" with values

### Step 2: Injection Vulnerabilities

**SQL Injection (CRITICAL):**
```python
# Vulnerable
query = f"SELECT * FROM users WHERE id = {user_input}"

# Safe
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

**Command Injection (CRITICAL):**
```python
# Vulnerable
os.system(f"ls {user_input}")

# Safe
subprocess.run(["ls", user_input], shell=False)
```

**XSS (HIGH):**
```javascript
// Vulnerable
innerHTML = user_input
dangerouslySetInnerHTML={{__html: userContent}}

// Safe
textContent = user_input
DOMPurify.sanitize(user_input)
```

### Step 3: Authentication/Authorization

**CRITICAL issues:** Hardcoded admin credentials, authentication bypass, missing authorization checks, JWT secrets in code.

**HIGH issues:** Weak password requirements, missing rate limiting on auth endpoints, session tokens in URLs, insecure cookie settings.

### Step 4: Data Exposure

**HIGH issues:** Logging sensitive data, error messages exposing internals, debug mode in production, stack traces returned to users, sensitive fields not excluded from API responses.

**MEDIUM issues:** Verbose error messages, comments containing sensitive info, TODO comments mentioning security fixes needed.

### Step 5: Dependency Check
If package files are in scope, check for known vulnerabilities (npm audit, pip-audit, govulncheck).

### Step 6: Generate Report
Compile findings into structured report (see Output Format below).

## Output Format

```
SECURITY REVIEW COMPLETE
========================

Verdict: [PASS / WARN / BLOCK]

CRITICAL Issues (must fix before commit):
- [file:line] [issue description]
  Remediation: [specific fix]

HIGH Issues (should fix before commit):
- [file:line] [issue description]
  Remediation: [specific fix]

MEDIUM Issues (recommended to fix):
- [file:line] [issue description]
  Remediation: [specific fix]

LOW Issues (for awareness):
- [file:line] [issue description]

Summary:
- [N] CRITICAL, [N] HIGH, [N] MEDIUM, [N] LOW
- Files reviewed: [N]
- [Verdict explanation]
```

## Integration with /committing-changes

When called from `/committing-changes` for public repository:
1. Receive list of staged files
2. Run full review (Mode A)
3. Return verdict to `/committing-changes`
4. If BLOCK: `/committing-changes` halts and shows remediation
5. If WARN: `/committing-changes` shows warning, asks for confirmation
6. If PASS: `/committing-changes` proceeds normally

## Red Flags -- STOP and Investigate

- Environment files (.env, .env.local) in staged changes
- Files named `secrets`, `credentials`, `config` with values
- Strings that look like Base64-encoded data
- URLs with embedded usernames/passwords
- Files with "DO NOT COMMIT" comments
- Private key file patterns (*.pem, *.key, id_rsa)

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "It's just a test key" | Test keys in public repos get scraped. Use env vars. |
| "I'll rotate it later" | Later never comes. Block now. |
| "This repo is private" | Repos get accidentally publicized. Protect now. |
| "It's encrypted" | Encrypted secrets with hardcoded keys aren't secure. |
| "Only I use this" | Public means anyone. No exceptions. |

## Error Recovery

**Recoverable errors:**
- Tool not available: Continue with manual review, note limitation
- File not readable: Skip file, note in report

**Blocking errors:**
- No files to review: Ask user to specify scope
- Git not available: Cannot determine staged files, ask for file list

## File Reference

- Skill: `plugins/commandbase-git-workflow/skills/reviewing-security/SKILL.md`
