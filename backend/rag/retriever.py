import time

from rag.embeddings import EmbeddingGenerator
from rag.vectordb import VectorDatabase


class Retriever:
    """
    Retrieves the most relevant document chunks
    from ChromaDB.
    """

    def __init__(self):
        self.embedder = EmbeddingGenerator()
        self.db = VectorDatabase()

    def retrieve(self, query, top_k=3):
        """
        Retrieve the top-k most relevant document chunks.
        """

        # -----------------------------
        # Generate Query Embedding
        # -----------------------------
        t1 = time.time()

        query_embedding = self.embedder.embed_query(query)

        embedding_time = time.time() - t1

        # -----------------------------
        # Search ChromaDB
        # -----------------------------
        t2 = time.time()

        results = self.db.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        db_time = time.time() - t2

        print(f"Embedding : {embedding_time:.2f} sec")
        print(f"ChromaDB  : {db_time:.2f} sec")

        return results