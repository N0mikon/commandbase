# Clone Management

Operational reference for securely cloning external repositories into temporary directories, handling edge cases, and cleaning up after analysis.

## Secure Clone Command

The hardened clone command protects against known attack vectors in untrusted repositories:

```bash
git -c core.symlinks=false \
    -c core.hooksPath=/dev/null \
    clone \
    --filter=blob:none \
    --no-checkout \
    --no-recurse-submodules \
    "$url" "$dest"
```

**Flag explanations:**
- `core.symlinks=false` — Prevents CVE-2024-32002 symlink attack where malicious repos use symlinks to write outside the working tree
- `core.hooksPath=/dev/null` — Prevents execution of any git hooks bundled in the repository
- `--filter=blob:none` — Blobless clone: downloads commits and trees but fetches file content on demand (fast initial clone)
- `--no-checkout` — Delays file materialization; we use `git show` to selectively read files
- `--no-recurse-submodules` — Prevents submodule-based attacks that could clone additional malicious repos

**All five flags are mandatory.** Never omit security flags, even for well-known repositories.

## Local Path Fallback

Local paths and some self-hosted git servers don't support partial clone (`--filter=blob:none`). Detect local sources and fall back to shallow clone:

```bash
# If URL is a local path or file:// protocol, use shallow clone instead
git -c core.symlinks=false \
    -c core.hooksPath=/dev/null \
    clone \
    --depth=1 \
    --no-recurse-submodules \
    "$url" "$dest"
```

**Detection:** A URL is local if it starts with:
- `/` (Unix absolute path)
- `./` or `../` (relative path)
- A drive letter followed by `:` or `:\` (e.g., `C:\repos\project`)
- `file://` protocol

Everything else (HTTPS, SSH, `git://`) uses the blobless clone.

## Temp Directory Creation

Use the MINGW-portable `mktemp` pattern:

```bash
CLONE_DIR=$(mktemp -d -t researching-repo.XXXXXX) || exit 1
```

This falls back through `$TMPDIR` -> `$TEMP` -> `$TMP` -> `/tmp`, which covers Linux, macOS, and Windows/MINGW environments.

The `researching-repo.` prefix makes it easy to identify and clean up orphaned clone directories.

## GitHub Shorthand Expansion

When input matches the pattern `^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$` (exactly one slash, no protocol prefix, no additional path segments), expand it to a full GitHub URL:

```
user/repo  ->  https://github.com/user/repo.git
```

**Do NOT expand** inputs that:
- Contain `://` (already a full URL)
- Start with `git@` (SSH URL)
- Contain more than one `/` after the protocol
- Start with `/`, `./`, or `../` (local paths)

## Post-Clone Security Verification

After cloning, verify no hooks are present:

```bash
ls "$CLONE_DIR/.git/hooks/"
```

If any hook files exist (pre-commit, post-checkout, etc.), remove them:

```bash
rm -f "$CLONE_DIR/.git/hooks/"*
```

This is a defense-in-depth measure. The `core.hooksPath=/dev/null` flag should prevent hook execution, but removing the files eliminates the risk entirely.

## Cleanup Pattern

After analysis is complete and the research file has been written, offer clone disposition using AskUserQuestion with three options:

1. **"Delete clone (default)"** — Remove the temp directory entirely
2. **"Keep at current location"** — Preserve the clone, display the full path
3. **"Move to a specific path"** — Let the user provide a destination directory

**Windows/MINGW note:** Git marks some files in `.git/` as read-only. Before removing the clone directory, make all files writable:

```bash
chmod -R +w "$CLONE_DIR" && rm -rf "$CLONE_DIR"
```

Without `chmod -R +w`, `rm -rf` will fail silently on read-only `.git` files.

## Error Handling

Common clone failure cases and how to handle them:

| Error | Symptom | Response |
|-------|---------|----------|
| **Authentication failure** | `fatal: could not read Username` or `Permission denied (publickey)` | Report clearly. Suggest checking SSH keys (`ssh -T git@github.com`) or using HTTPS URL instead. Do not attempt credential management. |
| **Network failure** | `fatal: unable to access` or timeout | Report the error. Suggest checking network connectivity. |
| **Invalid URL** | `fatal: repository not found` or malformed URL errors | Report the error. Ask user to verify the URL is correct. |
| **Repository not found** | HTTP 404 or `Repository not found` | Report that the repository doesn't exist or is private. Suggest checking the URL or repository permissions. |
| **Partial clone unsupported** | `fatal: the remote end hung up unexpectedly` with `--filter` | Fall back to shallow clone with `--depth=1`. This may happen with older git servers. |
