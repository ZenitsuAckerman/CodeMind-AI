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

## Frontend Sprint 1 (Landing Experience)
- **Status:** Completed ✅
- **Goals Achieved:**
  - Setup React 19 + Vite + Tailwind v4 + TypeScript architecture.
  - Implemented premium monochrome design system with a single blue accent.
  - Setup Geist and Geist Mono typography.
  - Created timeless landing page with Mock App Window product preview.
  - Avoided AI-marketing aesthetics in favor of developer-first styling.

## Frontend Sprint 2 (Application Shell)
- **Status:** Completed ✅
- **Goals Achieved:**
  - Designed and built the global `AppLayout` component with nested React Router.
  - Implemented collapsible `Sidebar` managed via Zustand.
  - Implemented minimalist `Header` with contextual `Breadcrumbs`.
  - Built custom `CommandPalette` (⌘K) using Framer Motion.
  - Structured modular components (`ui`, `layout`, `search`, `feedback`).
  - Authored frontend architecture documentation.

## Frontend Sprint 3 (Authentication Experience)
- **Status:** Completed ✅
- **Goals Achieved:**
  - Implemented global `useAuthStore` via Zustand for client auth state.
  - Set up Axios client with JWT request interceptors and 401 response interceptors.
  - Built strictly functional `AuthLayout` and `ProtectedRoute` components.
  - Created Login and Register views with `react-hook-form` and Zod validation.
  - Constructed accessible UI primitives (`Input`, `Label`).
  - Integrated Sonner toasts for API error feedback.

## Frontend Sprint 4 (Projects Experience)
- **Status:** Completed ✅
- **Goals Achieved:**
  - Integrated `@tanstack/react-query` globally for seamless server state and optimistic caching.
  - Built `Dashboard` view displaying project cards with inline delete capabilities.
  - Created `CreateProjectDialog` modal using `radix-ui/react-dialog` to maintain workspace context.
  - Set up `ProjectDetail` view as scaffolding for Sprint 5 (AI Chat and Document ingestion).
  - Developed `Card`, `Dialog`, and `Textarea` accessible UI primitives.
  - Connected `projectService.ts` API hooks to the backend.

## Frontend Sprint 5 (Knowledge Workspace)
- **Status:** Completed ✅
- **Goals Achieved:**
  - Rebuilt `ProjectDetail` into an IDE-like split-pane Knowledge Workspace interface.
  - Integrated `react-markdown` and `rehype-highlight` for syntax-highlighted code responses matching global dark/monochrome themes.
  - Built `CitationBadge` and `CitationModal` dialog to inspect vector store chunk citations.
  - Added repository index inspector panel displaying active embeddings and Qdrant status.
  - Built fixed prompt input area with auto-expansion and keyboard shortcuts (Enter to send, Shift+Enter for newline).
  - Created `chatService.ts` for handling RAG chat requests to the backend.

## Frontend Sprint 6 (Production Readiness)
- **Status:** Completed ✅
- **Goals Achieved:**
  - Implemented Route-Level Code Splitting (`React.lazy` and `Suspense`), reducing the initial `index.js` bundle size from >1000KB to ~323KB by lazily loading `ProjectDetail` and markdown parsers.
  - Added a global `<ErrorBoundary>` wrapper using `react-error-boundary` to gracefully catch and display application crashes using `<ErrorState>`.
  - Built a dedicated `NotFound` (404) route.
  - Tuned `TanStack Query` for production (`gcTime: 15m`, exponential backoff retries, skipping 401/403 retries).
  - Built an accessible `@radix-ui/react-dropdown-menu` primitive and integrated it into the `ProfilePlaceholder` with Theme and Logout actions.
  - Created `.env.example` and completely rewrote the global `README.md` for open-source / enterprise deployment readiness.
  - Linked Landing Page Auth buttons to React Router paths.
