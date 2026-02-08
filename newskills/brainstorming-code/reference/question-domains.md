# Question Domains Reference

This reference provides domain-specific direction question templates. Use these as starting points — adapt questions to the specific feature being brainstormed. Questions should probe DIRECTION, not implementation details.

## Visual Domain (Users SEE)

**Trigger:** UI components, dashboards, displays, views, pages, screens

**Default Topics:**
1. **Layout Approach** - How information is arranged and what paradigm to use
2. **Interaction Paradigm** - How users navigate, manipulate, and interact
3. **Visual States** - How the system communicates status visually
4. **Information Hierarchy** - What's prominent vs. secondary

**Direction Questions:**

Layout:
- "Cards, list, or table view?" → [Cards] [List] [Table] [You decide]
- "Dense with more info, or spacious with less?" → [Dense] [Spacious] [You decide]
- "Single column or multi-column?" → [Single] [Multi] [Responsive] [You decide]
- "Dashboard or detail view as the primary interface?" → [Dashboard overview] [Detail-first] [You decide]
- "Realtime updates or manual refresh?" → [Realtime] [Manual refresh] [Refresh on action] [You decide]

Interaction:
- "Click to expand, or navigate to detail page?" → [Expand in place] [New page] [Modal] [You decide]
- "Infinite scroll or pagination?" → [Infinite scroll] [Pagination] [Load more button] [You decide]
- "Drag-and-drop or form-based editing?" → [Drag-and-drop] [Forms] [Both] [You decide]

States:
- "Empty state: helpful message or call-to-action?" → [Message only] [CTA to create] [You decide]
- "Loading: skeleton, spinner, or progressive?" → [Skeleton] [Spinner] [Progressive] [You decide]

---

## API Domain (Users CALL)

**Trigger:** Endpoints, APIs, services, integrations, webhooks

**Default Topics:**
1. **Protocol Direction** - What communication paradigm to use
2. **Response Philosophy** - How data is structured and returned
3. **Error Approach** - How failures are communicated to consumers
4. **Versioning Strategy** - How changes are managed over time

**Direction Questions:**

Protocol:
- "REST or GraphQL?" → [REST] [GraphQL] [You decide]
- "Synchronous or asynchronous processing?" → [Sync] [Async] [Mix depending on operation] [You decide]
- "Webhook callbacks or polling for status?" → [Webhooks] [Polling] [Server-sent events] [You decide]

Response:
- "Return minimal data or include related resources?" → [Minimal] [Include related] [Configurable] [You decide]
- "Envelope wrapper or direct response?" → [Envelope {data, meta}] [Direct] [You decide]
- "Pagination style?" → [Offset/limit] [Cursor-based] [Page numbers] [You decide]

Errors:
- "Error detail level?" → [Code only] [Code + message] [Code + message + suggestions] [You decide]
- "Validation errors: first only or all at once?" → [First error] [All errors] [You decide]

Versioning:
- "URL versioning or header versioning?" → [URL (/v1/)] [Header] [You decide]

---

## CLI Domain (Users RUN)

**Trigger:** Commands, scripts, tools, utilities, automation

**Default Topics:**
1. **Interface Paradigm** - How the command is structured and invoked
2. **Output Philosophy** - How results are displayed to the user
3. **Feedback Approach** - How progress and status are communicated
4. **Error Recovery** - How failures are handled and communicated

**Direction Questions:**

Interface:
- "Interactive or scripted?" → [Interactive prompts] [Flags only] [Both modes] [You decide]
- "Single command or subcommands?" → [Single command] [Subcommands (git-style)] [You decide]
- "Short flags, long flags, or both?" → [Long only (--verbose)] [Both (-v/--verbose)] [You decide]
- "Positional args or named flags?" → [Positional] [Named flags] [Mix] [You decide]

Output:
- "Default output: human-readable or machine-parseable?" → [Human (pretty)] [Machine (JSON)] [Auto-detect TTY] [You decide]
- "Verbosity levels?" → [Quiet/normal only] [Quiet/normal/verbose] [Multiple -v flags] [You decide]

Feedback:
- "Long operations: silent, spinner, or progress bar?" → [Silent] [Spinner] [Progress bar] [You decide]

---

## Content Domain (Users READ)

**Trigger:** Documentation, help text, guides, notifications, messages

**Default Topics:**
1. **Structure Philosophy** - How content is organized and layered
2. **Tone Direction** - What communication style to use
3. **Navigation Approach** - How users find and move through content
4. **Content Lifecycle** - How content changes are managed

**Direction Questions:**

Structure:
- "Quick reference or comprehensive guide?" → [Quick reference] [Comprehensive] [Both with toggle] [You decide]
- "Inline examples or separate examples section?" → [Inline] [Separate] [Both] [You decide]
- "Static content or dynamic/generated?" → [Static] [Dynamic] [You decide]
- "Markdown or rich text editing?" → [Markdown] [Rich text (WYSIWYG)] [You decide]

Tone:
- "Formal or conversational?" → [Formal] [Conversational] [You decide]
- "Technical precision or accessibility first?" → [Technical] [Accessible] [Layered (simple → advanced)] [You decide]

---

## Organization Domain (Users ORGANIZE)

**Trigger:** Sorting, filtering, categorizing, managing, structuring data

**Default Topics:**
1. **Grouping Philosophy** - How items are categorized and related
2. **Naming Approach** - How things are identified and labeled
3. **Exception Strategy** - How edge cases and outliers are handled
4. **Bulk Operations** - How multiple items are handled at once

**Direction Questions:**

Grouping:
- "Primary grouping method?" → [By date] [By type] [By status] [User-defined] [You decide]
- "Allow multiple categories per item?" → [Single category] [Multiple tags] [You decide]
- "Flat structure or hierarchical?" → [Flat] [Hierarchical/nested] [You decide]
- "Tags or categories?" → [Free-form tags] [Predefined categories] [Both] [You decide]

Exceptions:
- "Items that don't fit categories?" → [Uncategorized bucket] [Force categorization] [Special 'Other'] [You decide]
- "Duplicate detection?" → [Automatic merge] [Flag for review] [Allow duplicates] [You decide]

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

**DON'T ask (belongs in /researching-code):**
- "What patterns does the codebase currently use?"
- "Should we use library X or library Y?"
- "What does the existing API look like?"
- Questions about existing code conventions

**DON'T ask (belongs in /designing-code):**
- "What should the API response schema look like?"
- "How should errors be handled internally?"
- "What's the component boundary between X and Y?"
- Specific architectural decisions that need research first

**DO ask (direction questions):**
- Which interaction paradigm? (REST vs GraphQL, cards vs table, interactive vs scripted)
- Which organizational philosophy? (flat vs hierarchical, tags vs categories)
- Which user experience approach? (dense vs spacious, realtime vs manual)
- Which communication style? (formal vs conversational, verbose vs minimal)
