# Common Implementation Patterns

Reference patterns for structuring implementation phases.

## Database Changes

1. Start with schema/migration
2. Add store methods
3. Update business logic
4. Expose via API
5. Update clients

## New Features

1. Research existing patterns first
2. Start with data model
3. Build backend logic
4. Add API endpoints
5. Implement UI last

## Refactoring

1. Document current behavior
2. Plan incremental changes
3. Maintain backwards compatibility
4. Include migration strategy

## Success Criteria Guidelines

Success criteria should be automated and verifiable:

- Commands that can be run: test commands, lint commands, etc.
- Specific files that should exist
- Code compilation/type checking
- Automated test suites
- API responses or CLI output verification

## Phase Structure

Each phase should follow this structure:

```markdown
## Phase N: [Descriptive Name]

### Overview
[What this phase accomplishes]

### Changes Required:

#### 1. [Component/File Group]
**File**: `path/to/file.ext`
**Changes**: [Summary of changes]

### Success Criteria:
- [ ] [Automated verification command]
- [ ] [Specific testable outcome]
```
