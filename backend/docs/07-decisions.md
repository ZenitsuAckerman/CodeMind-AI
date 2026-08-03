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
