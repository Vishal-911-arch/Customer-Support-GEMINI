from rag.retriever import Retriever

retriever = Retriever()

results = retriever.retrieve(
    "Explain the wing diagram",
    top_k=3
)

print(results["metadatas"][0])