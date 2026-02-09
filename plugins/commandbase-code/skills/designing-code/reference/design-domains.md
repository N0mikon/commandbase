# Design Domains Reference

Categories of architectural decisions and example questions for each domain. Use these as starting points — adapt to the specific feature being designed.

## API Design

**When:** Endpoints, function signatures, data contracts, integrations

**Decision areas:**
- Endpoint structure and naming
- Request/response format
- Authentication and authorization approach
- Versioning strategy
- Rate limiting and throttling

**Example AskUserQuestion options:**
- "API style?" -> [REST] [GraphQL] [tRPC] [You decide]
- "Authentication approach?" -> [JWT tokens] [Session cookies] [API keys] [OAuth2] [You decide]
- "Response format?" -> [JSON:API] [Custom envelope] [Direct response] [You decide]
- "Error response detail?" -> [Code only] [Code + message] [Code + message + suggestions] [You decide]

## Pattern Selection

**When:** Architectural patterns, data flow, state management choices

**Decision areas:**
- Overall architecture pattern
- Data flow direction
- Communication patterns between components
- State management approach
- Caching strategy

**Example AskUserQuestion options:**
- "Architecture pattern?" -> [Layered/MVC] [Event-driven] [Microservices] [Modular monolith] [You decide]
- "State management?" -> [Server-side sessions] [Client-side state] [Hybrid] [You decide]
- "Component communication?" -> [Direct imports] [Event bus] [Message queue] [You decide]
- "Caching approach?" -> [In-memory] [Redis/external] [HTTP cache headers] [No caching] [You decide]

## Error Strategy

**When:** Failure modes, recovery approaches, user-facing error handling

**Decision areas:**
- Error classification (recoverable vs fatal)
- Error propagation pattern
- User-facing error messages
- Logging and monitoring approach
- Retry and fallback behavior

**Example AskUserQuestion options:**
- "Error propagation?" -> [Exceptions/throw] [Result types] [Error codes] [You decide]
- "Failed operations?" -> [Retry automatically] [Prompt user to retry] [Fail fast] [You decide]
- "Validation errors?" -> [Return first error] [Return all errors] [You decide]
- "Unexpected errors?" -> [Generic message] [Technical details in dev] [Error ID for support] [You decide]

## Component Boundaries

**When:** Module organization, interface design, dependency direction

**Decision areas:**
- What constitutes a module/component
- Public vs internal interfaces
- Dependency direction rules
- Shared vs duplicated code decisions
- Plugin/extension points

**Example AskUserQuestion options:**
- "Module granularity?" -> [Feature-based] [Layer-based] [Domain-based] [You decide]
- "Shared utilities?" -> [Central shared lib] [Copy per module] [Extract when 3+ uses] [You decide]
- "Inter-module communication?" -> [Direct imports] [Interface contracts] [Event-based] [You decide]

## Data & State

**When:** Storage decisions, data flow, caching, synchronization

**Decision areas:**
- Primary data storage
- Data access patterns
- Schema design approach
- Migration strategy
- Backup and recovery

**Example AskUserQuestion options:**
- "Primary storage?" -> [PostgreSQL] [SQLite] [MongoDB] [File-based] [You decide]
- "ORM or raw queries?" -> [ORM (Prisma/Drizzle)] [Query builder (Knex)] [Raw SQL] [You decide]
- "Schema changes?" -> [Migration files] [Auto-sync] [You decide]
- "Data validation?" -> [Schema validation (Zod)] [Runtime checks] [Type system only] [You decide]
