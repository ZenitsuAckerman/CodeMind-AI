from typing import List, Dict, Any

class PromptBuilder:
    """
    Responsible for creating high-quality prompts to send to the LLM.
    """
    
    SYSTEM_PROMPT = """You are an AI Engineering Assistant.
Answer ONLY using the supplied context.
Never invent information.
If the answer is not contained in the retrieved context, reply that the information is unavailable.
Always answer clearly and concisely."""

    @staticmethod
    def build_rag_prompt(question: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
        """
        Constructs the final prompt string incorporating the system prompt, context, and user question.
        """
        context_parts = []
        for i, chunk in enumerate(retrieved_chunks):
            # We can label them so the LLM clearly sees the boundaries
            context_parts.append(f"--- Chunk {i+1} ---\n{chunk['content']}\n")
            
        context_string = "\n".join(context_parts)
        
        prompt = f"""{PromptBuilder.SYSTEM_PROMPT}

Retrieved Context:
{context_string}

User Question: {question}
"""
        return prompt
