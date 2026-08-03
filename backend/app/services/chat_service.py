import uuid
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.chat import ChatResponse, Citation
from app.services.retrieval_service import RetrievalService
from app.services.llm.prompt_builder import PromptBuilder
from app.services.llm.gemini_provider import gemini_provider

class ChatService:
    """
    Orchestrates the AI Chat workflow: retrieval -> prompt building -> LLM generation.
    """
    
    @staticmethod
    async def chat_with_project(db: AsyncSession, project_id: uuid.UUID, user_id: uuid.UUID, question: str) -> ChatResponse:
        if not gemini_provider:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI capabilities are not configured on this server."
            )
            
        # 1. Retrieve relevant chunks from Qdrant
        # The RetrievalService inherently enforces project ownership
        retrieved_chunks = await RetrievalService.search(
            db=db, 
            project_id=project_id, 
            user_id=user_id, 
            query=question, 
            limit=5
        )
        
        # 2. Map citations early
        citations = []
        for chunk in retrieved_chunks:
            citations.append(Citation(
                document_id=uuid.UUID(chunk["document_id"]),
                chunk_index=chunk["chunk_index"]
            ))
            
        # 3. Build the LLM Prompt
        prompt = PromptBuilder.build_rag_prompt(question=question, retrieved_chunks=retrieved_chunks)
        
        # 4. Call Gemini Provider
        answer = await gemini_provider.generate_answer(prompt)
        
        # 5. Return Answer and Citations
        return ChatResponse(
            answer=answer,
            citations=citations
        )
