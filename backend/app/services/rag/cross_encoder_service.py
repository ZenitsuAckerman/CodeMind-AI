from typing import List, Dict, Any
from sentence_transformers import CrossEncoder

class CrossEncoderService:
    """
    Reranks a list of candidate chunks based on their relevance to the query.
    Uses a cross-encoder model which is slower but much more accurate than bi-encoders.
    """
    def __init__(self, model_name: str = "BAAI/bge-reranker-base"):
        # Load the reranker into memory.
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, candidates: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Takes a question and a list of candidates (merged from BM25 and Vector search),
        scores them, and returns the top `limit` results.
        """
        if not candidates:
            return []
            
        # Prepare pairs for the CrossEncoder (query, text)
        pairs = [[query, candidate["content"]] for candidate in candidates]
        
        # Predict relevance scores
        scores = self.model.predict(pairs)
        
        # Attach scores back to candidates
        for i, candidate in enumerate(candidates):
            candidate["relevance_score"] = float(scores[i])
            
        # Sort by relevance_score descending
        candidates.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        # Return top N
        return candidates[:limit]

# Singleton instance ensures model is loaded only once
cross_encoder_service = CrossEncoderService()
