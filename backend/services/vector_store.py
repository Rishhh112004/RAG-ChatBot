import faiss
import numpy as np
import pickle
import os

INDEX_PATH = "vector_store/faiss.index"
META_PATH = "vector_store/metadata.pkl"


class VectorStore:

    def __init__(self, dimension=384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []

    def add_vectors(self, vectors, metadata):

        vectors = np.array(vectors).astype("float32")

        self.index.add(vectors)

        self.metadata.extend(metadata)

    def save(self):

        faiss.write_index(self.index, INDEX_PATH)

        with open(META_PATH, "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self):

        if os.path.exists(INDEX_PATH):

            self.index = faiss.read_index(INDEX_PATH)

            with open(META_PATH, "rb") as f:
                self.metadata = pickle.load(f)

    def search(self, query_vector, k=3):

        query_vector = np.array([query_vector]).astype("float32")

        distances, indices = self.index.search(query_vector, k)

        results = []

        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])

        return results