# Description Writing Guide

The description field is the most critical part of a skill. It determines when Claude invokes the skill - every other part of the skill is useless if the description doesn't trigger correctly.

## The Formula

```
"Use this skill when [primary situation]. This includes [specific use case with trigger keywords],
[another use case], [another use case], and [edge case or less obvious use case]."
```

The formula works because:
- "Use this skill when" primes Claude to match against user intent
- The primary situation captures the broadest trigger
- The specific use cases add keyword density for varied phrasings
- Edge cases prevent the skill from being overlooked in non-obvious situations

## The 4C Principles

Every description must satisfy all four:

**Clear** - No jargon, no vague terms, no ambiguity. A reader should understand the skill's scope in one pass. If you need domain-specific terms, pair them with plain-language equivalents.

**Concise** - 1-2 sentences for core functionality. The description has a 1024-character limit, but aim for 200-400 characters. Every word must earn its place.

**Contextual** - Describe the situations and scenarios where this skill activates. Think from Claude's perspective: "When a user says X, should I invoke this?" The description must answer that question.

**Complete** - Cover both the functionality (what it does) and the trigger conditions (when it activates). Missing either half means the skill either triggers incorrectly or not at all.

## Good Examples

### Example 1: Skill for deploying Lambda functions

```
"Use this skill when deploying AWS Lambda functions, updating Lambda configurations,
or troubleshooting Lambda deployment failures. This includes writing deployment scripts,
configuring environment variables, setting up API Gateway triggers, managing Lambda layers,
and debugging cold start or timeout issues."
```

**Why it works:**
- Primary situation: "deploying AWS Lambda functions" - broad trigger
- Three related activities: deploying, updating, troubleshooting
- Specific keywords: "deployment scripts", "API Gateway", "Lambda layers", "cold start"
- Edge case: "timeout issues" catches debugging scenarios

### Example 2: Skill for processing PDF documents

```
"Use this skill when extracting data from PDF files, converting PDFs to other formats,
or analyzing PDF content programmatically. This includes parsing tables from PDFs,
extracting text with layout preservation, splitting or merging PDF documents,
and handling encrypted or password-protected PDFs."
```

**Why it works:**
- Three distinct triggers: extracting, converting, analyzing
- Specific operations: "parsing tables", "layout preservation", "splitting or merging"
- Edge case: "encrypted or password-protected" catches a common stumbling point

### Example 3: Skill for managing Git workflows

```
"Use this skill when setting up Git branching strategies, resolving merge conflicts,
or configuring Git hooks and automation. This includes designing branch naming conventions,
writing pre-commit hooks, managing release branches, cherry-picking commits across branches,
and recovering from force-push mistakes."
```

**Why it works:**
- Covers setup, resolution, and configuration - three different entry points
- Action-oriented keywords: "designing", "writing", "managing", "cherry-picking", "recovering"
- Edge case: "force-push mistakes" catches a real pain point users actually search for

## Bad Examples and Fixes

### Bad Example 1: Too vague

```
"Helps with code tasks."
```

**Problems:** No trigger keywords, no specificity, Claude cannot distinguish this from any other coding skill. "Code tasks" matches everything and therefore matches nothing.

**Fixed:**
```
"Use this skill when refactoring Python code to improve readability, reduce complexity,
or follow PEP 8 conventions. This includes extracting functions, simplifying conditionals,
renaming variables for clarity, and reorganizing module structure."
```

### Bad Example 2: Too broad

```
"Use this skill for all Python-related tasks including writing, debugging, testing,
deploying, documenting, and maintaining Python applications."
```

**Problems:** Covers everything Python - Claude can't distinguish when to use this vs. its general Python knowledge. If a skill's scope is "everything", it adds no signal.

**Fixed:**
```
"Use this skill when writing Python CLI tools with argparse or click. This includes
setting up argument parsing, adding subcommands, handling stdin/stdout piping,
generating help text, and packaging CLI tools for distribution with setuptools."
```

### Bad Example 3: First person voice

```
"I help you write better documentation for your APIs by generating OpenAPI specs
and markdown docs."
```

**Problems:** First person voice ("I help you") doesn't match how Claude evaluates skill descriptions. The description should tell Claude about the skill, not speak as the skill.

**Fixed:**
```
"Use this skill when generating API documentation, creating OpenAPI specifications,
or writing markdown reference docs for REST endpoints. This includes documenting
request/response schemas, authentication flows, error codes, and rate limits."
```

### Bad Example 4: Describes WHAT but not WHEN

```
"A comprehensive skill for database management including migrations, queries, and backups."
```

**Problems:** Says what the skill contains but not when Claude should reach for it. "Comprehensive" and "including" are filler. No trigger conditions.

**Fixed:**
```
"Use this skill when writing database migrations, optimizing slow queries,
or setting up automated backup procedures. This includes creating migration scripts
for schema changes, analyzing query execution plans, configuring pg_dump schedules,
and handling data migration between database versions."
```

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Too vague | No trigger keywords for Claude to match | Add 3-5 specific operations as trigger words |
| Too broad | Matches everything, so Claude can't distinguish | Narrow to a specific domain or workflow |
| First person | Doesn't match Claude's evaluation pattern | Use third person: "Use this skill when..." |
| Missing trigger | Describes WHAT but not WHEN | Add situational context: "when [doing X]" |
| Keyword stuffing | Reads like a search engine trick, not guidance | Use natural language with embedded keywords |
| Duplicating Claude's knowledge | Describes what Claude already knows | Focus on project-specific or non-obvious patterns |

## Writing Process

Follow these steps to craft a description:

1. **List 5 situations** where a user would need this skill. Be specific - not "writing code" but "writing database migration scripts for PostgreSQL."

2. **Extract trigger keywords** from those situations. These are the words a user would actually say when asking for help.

3. **Write the description** using the formula. Start with the broadest trigger, then layer in specifics.

4. **Apply the 4C check:**
   - Clear? Can someone understand the scope in one read?
   - Concise? Is every word necessary?
   - Contextual? Does it describe WHEN, not just WHAT?
   - Complete? Are both functionality and triggers covered?

5. **Validate constraints:**
   - Under 1024 characters?
   - No angle brackets (`<` or `>`)?
   - Third person voice?
   - Starts with "Use this skill when..."?

6. **Test mentally:** Read the description and ask: "If a user said [trigger phrase], would Claude match this skill?" Try 3 different phrasings.
