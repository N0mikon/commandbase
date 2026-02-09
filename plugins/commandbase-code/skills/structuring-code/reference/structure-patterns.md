# Structure Patterns Reference

Common structural patterns to look for and follow when creating structural maps. Use these as recognition aids — always verify which patterns the actual codebase uses.

## File Placement Conventions

### Co-location
Files that work together live in the same directory.
```
features/auth/
  auth.controller.ts
  auth.service.ts
  auth.test.ts
  auth.types.ts
```
**When to follow:** Most modern frameworks. Default recommendation for greenfield.

### Separation by Type
Files grouped by their role across the whole app.
```
controllers/auth.controller.ts
services/auth.service.ts
tests/auth.test.ts
types/auth.types.ts
```
**When to follow:** Legacy projects, some backend conventions. Follow if existing.

### Hybrid
Top-level separation with co-located features inside.
```
src/
  features/auth/  (co-located)
  lib/            (shared utilities)
  types/          (shared types)
```
**When to follow:** Common in medium-large projects. Good balance.

## Module Boundary Patterns

### Barrel Exports
Each module has an index file that re-exports its public API.
- Internal files import freely within the module
- External consumers import only from the barrel
- Makes refactoring internals safe

### Feature Folders
Each feature is a self-contained directory with everything it needs.
- Routes, components, services, types, tests — all in one folder
- Shared code lives in a separate `shared/` or `lib/` directory
- Dependencies flow inward (features depend on shared, not on each other)

### Layer Architecture
Horizontal layers where each layer only imports from layers below.
- Presentation → Application → Domain → Infrastructure
- Strict dependency direction prevents circular imports

## Test Organization Patterns

### Co-located Tests
Test files live next to the code they test.
```
auth.service.ts
auth.service.test.ts
```
**Signal:** Look for `.test.ts` or `.spec.ts` files alongside source files.

### Mirror Tree
Test directory mirrors source directory structure.
```
src/auth/service.ts
tests/auth/service.test.ts
```
**Signal:** Look for a top-level `tests/` or `__tests__/` directory.

### By Test Type
Tests organized by type rather than by module.
```
tests/unit/auth.test.ts
tests/integration/auth-flow.test.ts
tests/e2e/login.test.ts
```
**Signal:** Look for `unit/`, `integration/`, `e2e/` subdirectories.

## Dependency Direction Rules

### Inward Dependencies
Feature modules depend on shared/core, never on each other.
```
feature-a → shared ← feature-b    (correct)
feature-a → feature-b              (violation)
```

### Layered Dependencies
Each layer depends only on the layer directly below.
```
routes → controllers → services → repositories    (correct)
routes → repositories                              (violation — skips layers)
```

### Interface Boundaries
Modules communicate through defined interfaces, not concrete implementations.
- Public types/interfaces exported from barrel
- Implementation details stay internal
- Dependency injection or factory patterns at boundaries

## Migration Sequencing Patterns

### Leaf-First
Start with modules that have no dependents, work inward.
- Safe: nothing depends on what you're changing
- Each step is independently deployable

### Interface-First
Define new interfaces first, then migrate implementations.
1. Create new interfaces alongside old ones
2. Update consumers to use new interfaces
3. Migrate implementations
4. Remove old interfaces

### Strangler Fig
Wrap old code with new code, gradually replacing.
1. Create new implementation beside old
2. Route traffic/imports to new code
3. Verify new code works
4. Remove old code

**When to use:** Large refactors where incremental replacement is safer than big-bang.
