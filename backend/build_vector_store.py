from services.text_processing import process_uploads
from services.embedding_service import EmbeddingService
from services.vector_store import VectorStore


def build_index():

    chunks = process_uploads()

    texts = [c["chunk_text"] for c in chunks]

    embedder = EmbeddingService()

    embeddings = embedder.embed_texts(texts)

    store = VectorStore()

    store.add_vectors(embeddings, chunks)

    store.save()

    print("Vector store built successfully")


if __name__ == "__main__":
    build_index()