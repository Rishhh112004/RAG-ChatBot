from sentence_transformers import SentenceTransformer

class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_texts(self, texts):
        """
        Convert list of texts into embeddings
        """
        embeddings = self.model.encode(texts)
        return embeddings

    def embed_query(self, query):
        """
        Convert a question into embedding
        """
        return self.model.encode([query])[0]