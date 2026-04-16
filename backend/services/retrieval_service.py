from backend.services.embedding_service import EmbeddingService
from backend.services.vector_store import VectorStore


class RetrievalService:

    def __init__(self):
        self.embedder = EmbeddingService()
        self.vector_store = VectorStore()
        self.vector_store.load()


    def retrieve(self, query, k=5):
        import numpy as np

        # Step 1: embed query
        query_vec = self.embedder.embed_query(query)

        # Step 2: FAISS search (FIXED)
        D, I = self.vector_store.index.search(np.array([query_vec]), k)

        results = []
        query_words = query.lower().split()

        for idx in I[0]:
            chunk = self.vector_store.chunks[idx]
            text = chunk["chunk_text"].lower()

            # remove weak chunks
            if len(text.split()) < 5:
                continue

            # keyword score
            keyword_score = sum(1 for word in query_words if word in text)

            # exact match boost
            if query.lower() in text:
                keyword_score += 5

            results.append({
                "chunk": chunk,
                "keyword_score": keyword_score
            })

        # fallback
        if not results:
            return [self.vector_store.chunks[i] for i in I[0][:2]]

        # sort
        results.sort(key=lambda x: x["keyword_score"], reverse=True)

        return [r["chunk"] for r in results[:3]]