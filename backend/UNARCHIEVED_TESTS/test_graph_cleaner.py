from rag.graph_cleaner import GraphCleaner

cleaner = GraphCleaner()

result = cleaner.clean(
    r"C:\Users\Vishal Sharma\Desktop\HAL-AI-Customer-Support\backend\artifacts\debug_regions\plot.png"
)

cleaner.save(
    result,
    r"C:\Users\Vishal Sharma\Desktop\HAL-AI-Customer-Support\backend\artifacts\debug_regions\curve_only.png"
)

print("Done")