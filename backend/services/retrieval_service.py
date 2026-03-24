from services.embedding_service import EmbeddingService
from services.vector_store import VectorStore


class RetrievalService:

    def __init__(self):
        self.embedder = EmbeddingService()
        self.vector_store = VectorStore()
        self.vector_store.load()

    def retrieve(self, question, k=3):
        """
        Retrieve top-k relevant chunks for a question
        """

        query_vector = self.embedder.embed_query(question)

        results = self.vector_store.search(query_vector, k)

        return results