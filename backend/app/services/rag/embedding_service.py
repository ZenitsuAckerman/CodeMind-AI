from typing import List
from sentence_transformers import SentenceTransformer

class EmbeddingService:
    """
    Generates embeddings for chunks and search queries using SentenceTransformers.
    """
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        # Load the model into memory. This runs locally on CPU (or GPU if available).
        self.model = SentenceTransformer(model_name)
        self.vector_size = self.model.get_sentence_embedding_dimension()

    def embed_text(self, text: str) -> List[float]:
        """
        Generates an embedding for a single text string.
        """
        # BGE models typically require a prefix for queries, but for standard RAG, 
        # standard encoding is often sufficient. We will use standard encode.
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.tolist()
        
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a batch of text strings.
        """
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        return embeddings.tolist()

# Singleton instance
embedding_service = EmbeddingService()
