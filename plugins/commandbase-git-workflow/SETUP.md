# commandbase-git-workflow Setup

## Required: Deny Rules

Plugins cannot inject deny rules into `~/.claude/settings.json`. For full commit enforcement, manually add these deny rules:

```json
{
  "permissions": {
    "deny": [
      "Bash(git add -A*)",
      "Bash(git add . *)",
      "Bash(git add .)",
      "Bash(git commit --no-verify*)",
      "Bash(git commit -n *)",
      "Bash(git push --force*)",
      "Bash(git push -f *)",
      "Bash(git reset --hard*)",
      "Bash(git checkout .)",
      "Bash(git restore .)",
      "Bash(git clean -f*)"
    ]
  }
}
```

These rules block destructive git operations that bypass the `/committing-changes` skill workflow.
