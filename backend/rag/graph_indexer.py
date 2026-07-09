from langchain_core.documents import Document

from rag.embeddings import EmbeddingGenerator
from rag.vectordb import VectorDatabase


class GraphIndexer:

    def __init__(self):

        self.embedder = EmbeddingGenerator()
        self.db = VectorDatabase()

    # ----------------------------------------------------------
    # Index one analyzed graph into ChromaDB
    # ----------------------------------------------------------

    def index(self, graph_json, document, page):

        print("\n========== GRAPH INDEXER ==========")

        graph_text = f"""
Graph Title:
{graph_json.get("title","")}

Engineering Domain:
{graph_json.get("engineering_domain","")}

Graph Type:
{graph_json.get("graph_type","")}

X Axis:
{graph_json.get("x_axis","")}

Y Axis:
{graph_json.get("y_axis","")}

Curve Names:
{", ".join(graph_json.get("curve_names", []))}

LLM Summary:
{graph_json.get("llm_summary","")}
"""

        doc = Document(

            page_content=graph_text,

            metadata={

                "type": "graph",

                "document": document,

                "page": page,

                "title": graph_json.get("title", "")

            }

        )

        print("Generating embedding...")

        embeddings = self.embedder.embed_documents([doc])

        print("Embedding length :", len(embeddings))

        added = self.db.add_documents(

            [doc],

            embeddings

        )

        print("Added =", added)

        print("Database count =", self.db.count())

        print("===================================")