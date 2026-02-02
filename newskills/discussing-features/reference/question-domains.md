# Question Domains Reference

This reference provides domain-specific question templates. Use these as starting points - adapt questions to the specific feature being discussed.

## Visual Domain (Users SEE)

**Trigger:** UI components, dashboards, displays, views, pages, screens

**Default Topics:**
1. **Layout & Density** - How information is arranged and spaced
2. **Interaction Patterns** - How users navigate and manipulate
3. **Visual States** - Loading, empty, error, success appearances
4. **Information Hierarchy** - What's prominent vs. secondary

**Example Questions:**

Layout:
- "Cards, list, or table view?" -> [Cards] [List] [Table] [You decide]
- "Dense with more info, or spacious with less?" -> [Dense] [Spacious] [You decide]
- "Single column or multi-column?" -> [Single] [Multi] [Responsive] [You decide]

Interaction:
- "Click to expand, or navigate to detail page?" -> [Expand in place] [New page] [Modal] [You decide]
- "Infinite scroll or pagination?" -> [Infinite scroll] [Pagination] [Load more button] [You decide]

States:
- "Empty state: helpful message or call-to-action?" -> [Message only] [CTA to create] [You decide]
- "Loading: skeleton, spinner, or progressive?" -> [Skeleton] [Spinner] [Progressive] [You decide]

---

## API Domain (Users CALL)

**Trigger:** Endpoints, APIs, services, integrations, webhooks

**Default Topics:**
1. **Response Format** - Structure and content of responses
2. **Error Handling** - How failures are communicated
3. **Authentication & Authorization** - Access control patterns
4. **Versioning & Compatibility** - How changes are managed

**Example Questions:**

Response:
- "Return minimal data or include related resources?" -> [Minimal] [Include related] [Configurable via params] [You decide]
- "Envelope wrapper or direct response?" -> [Envelope {data, meta}] [Direct] [You decide]
- "Pagination style?" -> [Offset/limit] [Cursor-based] [Page numbers] [You decide]

Errors:
- "Error detail level?" -> [Code only] [Code + message] [Code + message + suggestions] [You decide]
- "Validation errors: first only or all?" -> [First error] [All errors] [You decide]

---

## CLI Domain (Users RUN)

**Trigger:** Commands, scripts, tools, utilities, automation

**Default Topics:**
1. **Output Format** - How results are displayed
2. **Flag Design** - Command-line interface patterns
3. **Progress & Feedback** - How status is communicated
4. **Error Recovery** - How failures are handled

**Example Questions:**

Output:
- "Default output: human-readable or machine-parseable?" -> [Human (pretty)] [Machine (JSON)] [Auto-detect TTY] [You decide]
- "Verbosity levels?" -> [Quiet/normal only] [Quiet/normal/verbose] [Multiple -v flags] [You decide]

Flags:
- "Short flags, long flags, or both?" -> [Long only] [Both] [You decide]
- "Positional args or named flags?" -> [Positional] [Named] [Mix] [You decide]

Progress:
- "Long operations: silent, spinner, or progress bar?" -> [Silent] [Spinner] [Progress bar] [You decide]

---

## Content Domain (Users READ)

**Trigger:** Documentation, help text, guides, notifications, messages

**Default Topics:**
1. **Structure & Depth** - How content is organized
2. **Tone & Voice** - Communication style
3. **Navigation & Discovery** - How users find content
4. **Versioning** - How content changes are managed

**Example Questions:**

Structure:
- "Quick reference or comprehensive guide?" -> [Quick reference] [Comprehensive] [Both with toggle] [You decide]
- "Inline examples or separate examples section?" -> [Inline] [Separate] [Both] [You decide]

Tone:
- "Formal or conversational?" -> [Formal] [Conversational] [You decide]
- "Technical precision or accessibility first?" -> [Technical] [Accessible] [Layered (simple -> advanced)] [You decide]

---

## Organization Domain (Users ORGANIZE)

**Trigger:** Sorting, filtering, categorizing, managing, structuring data

**Default Topics:**
1. **Grouping Criteria** - How items are categorized
2. **Naming & Labels** - How things are identified
3. **Exception Handling** - What happens with edge cases
4. **Bulk Operations** - How multiple items are handled

**Example Questions:**

Grouping:
- "Primary grouping method?" -> [By date] [By type] [By status] [User-defined] [You decide]
- "Allow multiple categories per item?" -> [Single category] [Multiple tags] [You decide]

Exceptions:
- "Items that don't fit categories?" -> [Uncategorized bucket] [Force categorization] [Special 'Other'] [You decide]
- "Duplicate detection?" -> [Automatic merge] [Flag for review] [Allow duplicates] [You decide]

---

## Mixed Domain Handling

When a feature spans multiple domains:

1. **Identify dominant domain** - What's the PRIMARY user interaction?
2. **Use dominant domain topics** - Start with those questions
3. **Pull 1-2 topics from secondary domain** - Add relevant sub-questions

Example: "User settings page" = Visual (dominant) + API (data persistence)
- Lead with visual questions (layout, states)
- Add API question: "Settings save immediately or require explicit save?"

---

## Anti-Patterns

**DON'T ask:**
- Technical architecture questions (defer to /planning-codebases)
- Performance optimization questions (defer to planning)
- "Should we use library X?" (defer to research)
- Generic questions not specific to this feature

**DO ask:**
- User-observable behavior questions
- Visual and interaction preferences
- Error presentation (not error handling implementation)
- Output format preferences
