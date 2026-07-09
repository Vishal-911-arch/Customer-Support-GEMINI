from rag.retriever import Retriever

retriever = Retriever()

results = retriever.retrieve(

    "How to check hydraulic pressure?"

)

print(results)