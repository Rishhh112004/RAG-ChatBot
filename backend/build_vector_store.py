from backend.services.text_processing import process_uploads
from backend.services.embedding_service import EmbeddingService
from backend.services.vector_store import VectorStore
def build_vector_store():

    chunks = process_uploads()

    embedder = EmbeddingService()

    texts = [c["chunk_text"] for c in chunks]

    embeddings = embedder.embed_texts(texts)

    import faiss
    import numpy as np

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)

    index.add(np.array(embeddings))

    faiss.write_index(index, "vector_store.index")

    import pickle
    with open("chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

    print("Vector store built successfully")


# 👇 IMPORTANT
if __name__ == "__main__":
    build_vector_store()