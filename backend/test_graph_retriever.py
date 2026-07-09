from rag.graph_retriever import GraphRetriever

retriever = GraphRetriever()

question = "Explain the drag coefficient graph."

graph = retriever.retrieve(question)

print(graph)