# Architecture

*(To be implemented in future sprints)*

## High-Level Design
- Client applications (Web/CLI) communicate with the FastAPI backend over REST.
- The FastAPI backend uses an N-tier architecture:
  - `repositories/`: Contains all database interactions. Translates SQLAlchemy into internal models.
  - `services/`: Contains core business logic. Repositories are injected here.
  - `api/`: Exposes REST endpoints to interact with services.
- Asynchronous processing (Celery) will be introduced for document ingestion and embedding generation.

### LLM Layer (AI Chat)
- `GeminiProvider`: Dedicated service to handle communication with Google Gemini API securely.
- `PromptBuilder`: Responsible for formatting high-quality prompts merging context and instructions.
- `ChatService`: The primary orchestrator tying `RetrievalService`, `PromptBuilder`, and `GeminiProvider` together.

## RAG Component Architecture
- Document Parsers
- Chunking Strategy
- Embedding Model (e.g., SentenceTransformers, local models)
- Vector Store (e.g., Qdrant)
- LLM Integration (e.g., Google Gemini)
