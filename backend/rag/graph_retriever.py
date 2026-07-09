from rag.vectordb import VectorDatabase
from rag.embeddings import EmbeddingGenerator


class GraphRetriever:

    def __init__(self):

        self.db = VectorDatabase()
        self.embedder = EmbeddingGenerator()

        # Tune this after testing
        self.threshold = 0.45

    def retrieve(self, question, top_k=1):

        query_embedding = self.embedder.embed_query(question)

        results = self.db.collection.query(

            query_embeddings=[query_embedding],

            n_results=top_k,

            where={"type": "graph"},

            include=["documents", "metadatas", "distances"]

        )

        if not results["documents"]:
            return None

        if len(results["documents"][0]) == 0:
            return None

        distance = results["distances"][0][0]

        print(f"\nGraph Distance : {distance}")

        # Reject poor matches
        if distance > self.threshold:

            print("No graph matched.")

            return None

        meta = results["metadatas"][0][0]

        graph = {

            "text": results["documents"][0][0],

            "document": meta.get("document", ""),

            "page": meta.get("page", ""),

            "title": meta.get("title", ""),

            "metadata": meta,

            "distance": distance

        }

        print("✓ Graph Retrieved")

        return graph