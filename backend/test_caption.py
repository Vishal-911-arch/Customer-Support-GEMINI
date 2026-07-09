from rag.vectordb import VectorDatabase

db = VectorDatabase()

data = db.collection.get()

graphs = []

for doc, meta in zip(data["documents"], data["metadatas"]):

    if meta.get("type") == "graph":

        graphs.append(meta)

print("Graphs =", len(graphs))

for g in graphs:
    print(g)