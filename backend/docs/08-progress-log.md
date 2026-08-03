# Progress Log

## Sprint 1
- **Status:** Completed ✅
- **Goals Achieved:**
  - Setup base FastAPI structure.
  - Setup Pydantic V2 config management.
  - Configured centralized logging.
  - Setup SQLAlchemy 2.x Async setup.
  - Added `/` and `/health` endpoints.
  - Created documentation skeletons.

## Sprint 2
- **Status:** Completed ✅
- **Goals Achieved:**
  - Implemented User model and migrations.
  - Implemented bcrypt password hashing and JWT issuance.
  - Implemented Auth endpoints (`/register`, `/login`, `/me`).

## Sprint 3
- **Status:** Completed ✅
- **Goals Achieved:**
  - Implemented Project model linked to Users.
  - Implemented full CRUD API for Projects.
  - Enforced ownership and permission checking at the Service layer.
  - Implemented strict input validation via Pydantic constraints.

## Milestone 2
- **Status:** Completed ✅
- **Goals Achieved:**
  - Implemented Document model linked to Projects.
  - Set up `StorageService` for local asynchronous file handling.
  - Exposed file upload endpoints (`python-multipart`).
  - Added strict file type and 25 MB size limits.

## Sprint 4
- **Status:** Completed ✅
- **Goals Achieved:**
  - Implemented DocumentContent model for storing raw text.
  - Developed TextExtractionService handling PDFs, DOCX, plaintext, and YAML.
  - Developed DocumentProcessingService to coordinate text extraction and update statuses.
  - Added `/process` endpoint for async processing imitation.

## Sprint 5 (Core RAG Pipeline)
- **Status:** Completed ✅
- **Goals Achieved:**
  - Built custom `ChunkingService` using Hugging Face tokenizers.
  - Integrated `SentenceTransformers` for local text embedding (`BAAI/bge-small-en-v1.5`).
  - Integrated `Qdrant` for vector storage and semantic search.
  - Built `/index` endpoint for pipeline orchestration.
  - Built `/search` endpoint for semantic chunk retrieval.

## Sprint 6 (AI Chat Layer)
- **Status:** Completed ✅
- **Goals Achieved:**
  - Integrated Google Gemini via `google-generativeai`.
  - Built `GeminiProvider`, `PromptBuilder`, and `ChatService`.
  - Added strict system prompts to prevent hallucination.
  - Built `/chat` endpoint supporting citations linked to source chunks.

## Sprint 7 (Advanced Retrieval Pipeline)
- **Status:** Completed ✅
- **Goals Achieved:**
  - Added `rank-bm25` for sparse keyword search.
  - Added `BAAI/bge-reranker-base` cross-encoder for precise reranking.
  - Implemented Hybrid Search in `RetrievalService` (Qdrant Top 20 + BM25 Top 20).
  - Merged, deduplicated, and reranked candidates to return the best Top 5 chunks.
