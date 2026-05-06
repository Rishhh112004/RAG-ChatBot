import faiss
import pickle
import os

class VectorStore:

    def __init__(self):
        self.index = None
        self.chunks = None

    def load(self):
        # Load FAISS index
        if os.path.exists("vector_store.index"):
            self.index = faiss.read_index("vector_store.index")
        else:
            raise Exception("FAISS index not found")

        if os.path.exists("chunks.pkl"):
            with open("chunks.pkl", "rb") as f:
                self.chunks = pickle.load(f)
        else:
            raise Exception("chunks.pkl not found")