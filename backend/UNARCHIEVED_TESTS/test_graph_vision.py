from rag.graph_analyzer import GraphAnalyzer

graph = GraphAnalyzer()

crop = graph.crop_graph(
    "Basic_Aerodynamics",
    17
)

print("\nRunning Vision...\n")

result = graph.understand_graph(crop)

print(result)