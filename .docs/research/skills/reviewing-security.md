# Research: reviewing-security Skill

## Overview

The `reviewing-security` skill (`~/.claude/skills/reviewing-security/SKILL.md`) reviews code for security vulnerabilities before committing to public repositories. It produces a verdict (PASS/WARN/BLOCK) based on severity of issues found.

**Trigger phrases**: `/review-security`, `security review`, `check for secrets`, `is this safe to commit publicly`

## The Iron Law

```
NO PUBLIC COMMIT WITH CRITICAL SECURITY ISSUES
```

If CRITICAL issues are found, the commit must be blocked. Secrets in public repos cannot be unlearned by the internet.

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

## Detection Patterns

### Secrets (CRITICAL)
```regex
api[_-]?key\s*[:=]\s*['"][a-zA-Z0-9]{16,}
AKIA[0-9A-Z]{16}
-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----
password\s*[:=]\s*['"][^'"]+['"]
(mongodb|postgresql|mysql|redis):\/\/[^:]+:[^@]+@
```

### Injection Vulnerabilities (CRITICAL)
**SQL Injection:**
```python
# Vulnerable
query = f"SELECT * FROM users WHERE id = {user_input}"

# Safe
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

**Command Injection:**
```python
# Vulnerable
os.system(f"ls {user_input}")

# Safe
subprocess.run(["ls", user_input], shell=False)
```

### XSS (HIGH)
```javascript
// Vulnerable
innerHTML = user_input
dangerouslySetInnerHTML={{__html: userContent}}

// Safe
textContent = user_input
DOMPurify.sanitize(user_input)
```

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

Summary:
- [N] CRITICAL, [N] HIGH, [N] MEDIUM, [N] LOW
- Files reviewed: [N]
```

## Integration with /committing-changes

When called from `/committing-changes` for public repository:
1. Receive list of staged files
2. Run full review (Mode A)
3. Return verdict
4. If BLOCK: `/committing-changes` halts
5. If WARN: Ask for confirmation
6. If PASS: Proceed normally

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "It's just a test key" | Test keys get scraped. Use env vars. |
| "I'll rotate it later" | Later never comes. Block now. |
| "This repo is private" | Repos get accidentally publicized. |
| "It's encrypted" | Encrypted with hardcoded keys isn't secure. |

## File Reference

- Main: `~/.claude/skills/reviewing-security/SKILL.md`
