# Capture Routing Rules

How to determine where a captured note goes based on vault conventions.

## Routing Decision Tree

```
1. Read vault CLAUDE.md for folder structure and conventions
2. Determine note type from capture mode:
   - Fleeting note → inbox/triage folder
   - Web capture → resources or references folder
   - Meeting/log → daily or meetings folder
   - Inbox processing → route to proper folder based on content
3. Apply vault-specific overrides from CLAUDE.md
4. If no clear destination → default to inbox/triage
```

## Default Routing Table

These are sensible defaults. The vault's CLAUDE.md conventions ALWAYS override these.

| Capture Mode | Default Destination | Frontmatter Type |
|-------------|-------------------|-----------------|
| Fleeting note | `inbox/` or `triage/` | `type: fleeting` |
| Web capture | `resources/` or `references/` | `type: resource` |
| Meeting note | `meetings/` or `daily/` | `type: meeting` |
| Log entry | `daily/` or `journal/` | `type: log` |
| Inbox processing | (varies by content) | (varies) |

## Minimal Frontmatter for Captured Notes

Every captured note gets at minimum:

```yaml
---
type: [fleeting/resource/meeting/log]
created: [ISO date]
tags: []
source: [where it came from]
status: inbox
---
```

Additional properties depend on the vault's schema. Read CLAUDE.md before adding vault-specific properties.

## Routing by Content Analysis

When processing inbox items (Mode D), analyze note content to determine routing:

1. **Check existing tags**: Tags suggest topic area → route to matching topic folder
2. **Check title keywords**: Meeting-related words → meetings folder, project names → project folder
3. **Check frontmatter type**: If `type` is set, route to the folder for that type
4. **Check creation context**: Daily notes → daily folder, reference material → resources
5. **When ambiguous**: Present options to user, don't auto-route

## Naming Captured Notes

| Mode | Naming Convention |
|------|------------------|
| Fleeting | `[date]-[brief-slug].md` (e.g., `2026-02-12-api-rate-limits.md`) |
| Web capture | `[source-title-slug].md` (e.g., `react-server-components-guide.md`) |
| Meeting | `[date]-[meeting-name].md` (e.g., `2026-02-12-sprint-planning.md`) |
| Log | `[date].md` or `[date]-[topic].md` |

Always use kebab-case. No spaces, no special characters.

## Source Attribution

For web captures, always include source attribution:

```yaml
---
source: "https://example.com/article"
captured: 2026-02-12
---
```

And in the note body:
```markdown
> [!info] Source
> Captured from [Article Title](https://example.com/article) on 2026-02-12
```

## Conflict Resolution

If a note with the same name already exists at the destination:

1. Check if it's a duplicate (same content) → warn user, don't create
2. If different content → append timestamp to name: `[name]-[timestamp].md`
3. Always inform the user of the conflict and resolution
