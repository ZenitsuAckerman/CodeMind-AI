from typing import List, Dict, Any
from rank_bm25 import BM25Okapi

class BM25Service:
    """
    Provides lightweight, in-memory BM25 keyword search capabilities.
    For production scale, this should be offloaded to Elasticsearch or Qdrant native sparse vectors.
    """
    
    @staticmethod
    def _tokenize(text: str) -> List[str]:
        # Simple whitespace/punctuation tokenizer for BM25
        return text.lower().replace('.', ' ').replace(',', ' ').split()

    @staticmethod
    def search(query: str, db_chunks: List[Dict[str, Any]], limit: int = 20) -> List[Dict[str, Any]]:
        """
        Takes a list of chunk dictionaries (representing all chunks for a project), 
        scores them using BM25 against the query, and returns the top candidates.
        """
        if not db_chunks:
            return []
            
        tokenized_corpus = [BM25Service._tokenize(chunk["content"]) for chunk in db_chunks]
        bm25 = BM25Okapi(tokenized_corpus)
        
        tokenized_query = BM25Service._tokenize(query)
        
        # Get scores
        doc_scores = bm25.get_scores(tokenized_query)
        
        # Pair chunks with scores
        scored_chunks = list(zip(doc_scores, db_chunks))
        
        # Sort by score descending
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        
        # Return top N that have a score > 0
        results = []
        for score, chunk in scored_chunks[:limit]:
            if score > 0:
                results.append({
                    "chunk_id": str(chunk["chunk_id"]),
                    "document_id": str(chunk["document_id"]),
                    "content": chunk["content"],
                    "chunk_index": chunk["chunk_index"],
                    "score": score
                })
                
        return results

# Expose a singleton-like interface if needed, though methods are static right now.
bm25_service = BM25Service()
