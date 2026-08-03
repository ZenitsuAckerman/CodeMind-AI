import uuid
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from app.services.rag.embedding_service import embedding_service

class QdrantService:
    """
    Integrates with Qdrant for storing and retrieving document vectors.
    """
    def __init__(self, collection_name: str = "document_chunks"):
        self.collection_name = collection_name
        # Use an in-memory database for local development ease, 
        # or switch to a persistent path/remote URL via config in production.
        self.client = QdrantClient(":memory:")
        self._ensure_collection()

    def _ensure_collection(self):
        """
        Creates the collection if it doesn't exist.
        """
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=embedding_service.vector_size, 
                    distance=Distance.COSINE
                )
            )

    def store_chunks(self, chunks_data: List[Dict[str, Any]]):
        """
        Stores a batch of chunks and their embeddings into Qdrant.
        chunks_data should contain: chunk_id, project_id, document_id, content, chunk_index, embedding
        """
        points = []
        for data in chunks_data:
            points.append(
                PointStruct(
                    id=str(data["chunk_id"]),
                    vector=data["embedding"],
                    payload={
                        "project_id": str(data["project_id"]),
                        "document_id": str(data["document_id"]),
                        "content": data["content"],
                        "chunk_index": data["chunk_index"]
                    }
                )
            )
            
        if points:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

    def search(self, project_id: uuid.UUID, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieves the most semantically similar chunks for a specific project.
        """
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="project_id",
                        match=MatchValue(value=str(project_id))
                    )
                ]
            ),
            limit=limit
        )
        
        results = []
        for hit in search_result:
            results.append({
                "chunk_id": hit.id,
                "score": hit.score,
                "document_id": hit.payload["document_id"],
                "content": hit.payload["content"],
                "chunk_index": hit.payload["chunk_index"]
            })
            
        return results

# Singleton instance
qdrant_service = QdrantService()
