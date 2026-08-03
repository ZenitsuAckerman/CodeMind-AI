# Architectural Decisions Record (ADR)

## Sprint 1

### ADR-001: Use FastAPI
- **Status:** Accepted
- **Context:** Need a high-performance, async-capable Python web framework.
- **Decision:** Use FastAPI for built-in validation, OpenAPI docs, and async support.

### ADR-002: Use Async SQLAlchemy & AsyncPG
- **Status:** Accepted
- **Context:** FastAPI shines with async operations; blocking DB calls negate this benefit.
- **Decision:** Use SQLAlchemy 2.x async features with asyncpg.

## Sprint 3

### ADR-003: Simple User-to-Project Relationship
- **Status:** Accepted
- **Context:** Need a way to organize assets. We could introduce complex Workspaces/Organizations with RBAC.
- **Decision:** For Version 1, we map Projects directly to Users (`owner_id`). We will forgo complex Workspaces to ship faster and reduce initial complexity.
