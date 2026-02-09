---
name: reviewing-security
description: "Use this skill when reviewing code for security vulnerabilities before committing to public repositories. This includes scanning for hardcoded secrets and API keys, checking for SQL injection and XSS vulnerabilities, validating input sanitization, detecting OWASP Top 10 issues, and reviewing authentication/authorization logic. Trigger phrases: '/review-security', 'security review', 'check for secrets', 'is this safe to commit publicly'."
allowed-tools: Read, Grep, Glob, LS, Bash, AskUserQuestion
---

# Security Review

You are reviewing code for security vulnerabilities before it becomes public. This skill activates before commits to public repositories and produces a security verdict: PASS, WARN, or BLOCK.

**Violating the letter of these rules is violating the spirit of these rules.**

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

```
BEFORE issuing a verdict:

1. SCOPE: Identify files to review (staged files or specified paths)
2. SCAN: Run automated secret detection
3. REVIEW: Manual inspection for each vulnerability category
4. CLASSIFY: Categorize findings by severity
5. VERDICT: PASS (no issues), WARN (medium only), or BLOCK (critical/high found)
6. ONLY THEN: Report findings with remediation guidance

Skip any step = missed vulnerabilities
```

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| **CRITICAL** | Immediate exploit risk, secrets exposed | BLOCK commit |
| **HIGH** | Serious vulnerability, likely exploitable | BLOCK commit |
| **MEDIUM** | Potential issue, context-dependent | WARN, recommend fix |
| **LOW** | Best practice violation, minor concern | Note for awareness |

## Initial Response

When invoked, first gather context:

1. Determine scope: staged files, specific files, or full diff
2. Check if repo is public or will become public
3. Present the review plan:

```
Security Review
===============
Scope: [N files to review]
Repository: [public/private]
Mode: [full/quick]

Proceeding with security scan...
```

## Modes

### Mode A: Full Review (Default for Public Repos)

Use for commits to public repositories or when explicitly requested.

**Checks all categories:**
1. Secrets and credentials
2. Injection vulnerabilities
3. Authentication/authorization
4. Data exposure
5. Dependency vulnerabilities
6. Code quality security

### Mode B: Quick Scan

Use for private repos or when user requests speed over thoroughness.

**Checks critical categories only:**
1. Secrets and credentials
2. Obvious injection vulnerabilities

## Process

### Step 1: Secret Detection

Scan for hardcoded secrets, API keys, and credentials.

**Patterns to detect:**

```
CRITICAL - Block immediately:
- API keys: api[_-]?key\s*[:=]\s*['\"][a-zA-Z0-9]{16,}
- AWS keys: AKIA[0-9A-Z]{16}
- Private keys: -----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----
- Passwords: password\s*[:=]\s*['"][^'"]+['"]
- Tokens: (bearer|token|auth)\s*[:=]\s*['"][a-zA-Z0-9\-_.]+['"]
- Connection strings: (mongodb|postgresql|mysql|redis):\/\/[^:]+:[^@]+@
- .env contents committed (not in .gitignore)

HIGH - Review carefully:
- Hardcoded URLs with credentials
- Base64-encoded strings that decode to secrets
- Comments containing "password", "secret", "key" with values
```

**Verification:**
```bash
# Search for common secret patterns in staged files
git diff --cached --name-only | xargs grep -lE "(api[_-]?key|password|secret|token|AKIA)" 2>/dev/null
```

### Step 2: Injection Vulnerabilities

Check for SQL injection, command injection, and XSS.

**SQL Injection (CRITICAL):**
```
# Vulnerable patterns:
query = f"SELECT * FROM users WHERE id = {user_input}"
cursor.execute("SELECT * FROM users WHERE name = '" + name + "'")

# Safe patterns:
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
cursor.execute("SELECT * FROM users WHERE id = %(id)s", {"id": user_id})
```

**Command Injection (CRITICAL):**
```
# Vulnerable patterns:
os.system(f"ls {user_input}")
subprocess.call(f"rm {filename}", shell=True)
exec(user_code)
eval(user_expression)

# Safe patterns:
subprocess.run(["ls", user_input], shell=False)
```

**XSS - Cross-Site Scripting (HIGH):**
```
# Vulnerable patterns:
innerHTML = user_input
document.write(user_data)
dangerouslySetInnerHTML={{__html: userContent}}

# Safe patterns:
textContent = user_input  # Escaped automatically
DOMPurify.sanitize(user_input)
```

### Step 3: Authentication/Authorization

Check for auth-related vulnerabilities.

**CRITICAL issues:**
- Hardcoded admin credentials
- Authentication bypass (always-true conditions)
- Missing authorization checks on sensitive endpoints
- JWT secrets in code

**HIGH issues:**
- Weak password requirements
- Missing rate limiting on auth endpoints
- Session tokens in URLs
- Insecure cookie settings (missing HttpOnly, Secure, SameSite)

### Step 4: Data Exposure

Check for sensitive data leakage.

**HIGH issues:**
- Logging sensitive data (passwords, tokens, PII)
- Error messages exposing internal details
- Debug mode enabled in production config
- Stack traces returned to users
- Sensitive fields not excluded from API responses

**MEDIUM issues:**
- Verbose error messages
- Comments containing sensitive information
- TODO comments mentioning security fixes needed

### Step 5: Dependency Check

If package files are in scope, check for known vulnerabilities.

```bash
# For Node.js
npm audit --json 2>/dev/null | head -100

# For Python
pip-audit 2>/dev/null || safety check 2>/dev/null

# For Go
govulncheck ./... 2>/dev/null
```

### Step 6: Generate Report

Compile findings into structured report.

## Output Format

```
SECURITY REVIEW COMPLETE
========================

Verdict: [PASS / WARN / BLOCK]

[If BLOCK or WARN, show findings:]

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

[If BLOCK:]
Commit blocked. Fix CRITICAL and HIGH issues before proceeding.

[If WARN:]
Proceed with caution. Consider fixing MEDIUM issues.

[If PASS:]
No security issues detected. Safe to commit.
```

## Error Recovery

**Recoverable errors:**
- Tool not available: Continue with manual review, note limitation
- File not readable: Skip file, note in report

**Blocking errors:**
- No files to review: Ask user to specify scope
- Git not available: Cannot determine staged files, ask for file list

## Red Flags - STOP and Investigate

If you notice any of these, investigate thoroughly:

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

## Integration with /committing-changes

When called from `/committing-changes` for a public repository:

1. Receive list of staged files
2. Run full review (Mode A)
3. Return verdict to `/committing-changes`
4. If BLOCK: `/committing-changes` halts and shows remediation
5. If WARN: `/committing-changes` shows warning, asks for confirmation
6. If PASS: `/committing-changes` proceeds normally

## The Bottom Line

**No secrets in public repos. No unvalidated input in queries. No exceptions.**

Scan thoroughly. Report clearly. Block when necessary. This is non-negotiable. Every public commit. Every time.
