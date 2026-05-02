import re
import numpy as np
from backend.services.embedding_service import EmbeddingService
from backend.services.vector_store import VectorStore
from backend.services.query_rewriter import rewrite_query

# rank_bm25 is added 
from rank_bm25 import BM25Okapi

def _tokenize(text: str) -> list:
    """Simple whitespace + lowercase tokenizer for BM25."""
    return re.findall(r"\w+", text.lower())


class RetrievalService:

    def __init__(self):
        self.embedder = EmbeddingService()
        self.vector_store = VectorStore()
        self.vector_store.load()

        self._build_bm25()

    def _build_bm25(self):
        """Build BM25 index from loaded chunks."""
        if not self.vector_store.chunks:
            self.bm25 = None
            return
        tokenized = [_tokenize(c["chunk_text"]) for c in self.vector_store.chunks]
        self.bm25 = BM25Okapi(tokenized)

    def retrieve(self, query: str, k: int = 10) -> list:

        # Step 1: Clean query (remove filler words)
        cleaned = rewrite_query(query)

        # --- FAISS semantic search ---
        query_vec = self.embedder.embed_query(cleaned)
        D, I = self.vector_store.index.search(np.array([query_vec]), k)

        # Build FAISS score map: chunk_index → semantic_score
        faiss_scores = {}
        for rank, idx in enumerate(I[0]):
            if idx < 0 or idx >= len(self.vector_store.chunks):
                continue
            faiss_scores[int(idx)] = 1 / (1 + D[0][rank])

        # --- BM25 keyword search ---
        bm25_scores = {}
        if self.bm25 is not None:
            tokens = _tokenize(cleaned)
            raw_scores = self.bm25.get_scores(tokens)

            # Normalize BM25 scores to [0, 1]
            max_bm25 = max(raw_scores) if max(raw_scores) > 0 else 1.0
            for idx, score in enumerate(raw_scores):
                bm25_scores[idx] = score / max_bm25

        original_tokens = _tokenize(query)
        phrase_bonus_map = {}
        for idx, chunk in enumerate(self.vector_store.chunks):
            text = chunk["chunk_text"].lower()
            bonus = 0.0
            for n in (3, 2):
                for i in range(len(original_tokens) - n + 1):
                    phrase = " ".join(original_tokens[i:i+n])
                    if all(len(w) >= 3 for w in original_tokens[i:i+n]):
                        if phrase in text:
                            bonus = 0.3
                            break
                if bonus:
                    break
            if bonus:
                phrase_bonus_map[idx] = bonus

        # --- Combine all scores ---
        if self.bm25 is not None:
            # Get top-k BM25 indices
            top_bm25 = sorted(bm25_scores.keys(),
                              key=lambda x: bm25_scores[x], reverse=True)[:k]
        else:
            top_bm25 = []

        all_candidates = set(faiss_scores.keys()) | set(top_bm25)

        results = []
        for idx in all_candidates:
            semantic = faiss_scores.get(idx, 0.0)
            bm25 = bm25_scores.get(idx, 0.0)
            phrase = phrase_bonus_map.get(idx, 0.0)
            
            final_score = (
                0.50 * semantic +
                0.35 * bm25 +
                0.15 * phrase
            )

            results.append({
                "chunk": self.vector_store.chunks[idx],
                "score": final_score
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        return [r["chunk"] for r in results[:4]]

    def reload(self):

        self.vector_store.load()
        self._build_bm25()