# RAG Pipeline

This document outlines the specifics of our Retrieval-Augmented Generation approach.

## Extraction Phase
- Documents are parsed using Extractor architecture (PyMuPDF, python-docx, PyYAML, etc.).
- Text is stored entirely in the `document_contents` table prior to chunking.

## Indexing Phase
- **Chunking**: Custom `ChunkingService` splits text by paragraphs and sentences, aiming for ~500 tokens with 100 token overlap. Token counting is accurately done using the Hugging Face `transformers` tokenizer.
- **PostgreSQL**: Chunks are persisted to the `document_chunks` table for permanent storage.
- **Embeddings**: `SentenceTransformer("BAAI/bge-small-en-v1.5")` is executed locally in memory to embed the chunks into dense vectors.
- **Qdrant**: Vectors are upserted into an in-memory/local Qdrant instance.

## Retrieval Phase (Hybrid Search + Reranking)
1. **Dense Retrieval (Vector Search)**: 
   - A query is embedded using `BAAI/bge-small-en-v1.5`.
   - Qdrant is queried (hard-filtered by `project_id`) to return the Top 20 semantic chunks.
2. **Sparse Retrieval (Keyword Search)**:
   - All chunks for the project are loaded from PostgreSQL into memory.
   - The query is tokenized and scored against the chunks using `BM25Okapi` (`rank-bm25`).
   - The Top 20 keyword chunks are returned.
3. **Merging**:
   - Both candidate lists are merged and deduplicated by `chunk_id`.
4. **Cross-Encoder Reranking**:
   - The merged list is passed to `CrossEncoder("BAAI/bge-reranker-base")`.
   - Every candidate is individually scored against the user query.
   - The absolute best Top 5 chunks are returned for generation.

## Generation Phase (AI Chat)
- The retrieved chunks are concatenated by the `PromptBuilder`.
- A strict system prompt is applied to prevent hallucination.
- The prompt is sent to Google's Gemini model via the `GeminiProvider`.
- The answer and citations are returned to the user.

## Components to define (Future)
- Reranking
- Conversation Memory
