from rag.graph_grid import GraphGrid

grid = GraphGrid()

result = grid.remove_grid(
    r"artifacts/debug_regions/plot.png"
)

grid.save(
    result["binary"],
    r"artifacts/debug_regions/1_binary.png"
)

grid.save(
    result["horizontal"],
    r"artifacts/debug_regions/2_horizontal.png"
)

grid.save(
    result["vertical"],
    r"artifacts/debug_regions/3_vertical.png"
)

grid.save(
    result["grid"],
    r"artifacts/debug_regions/4_grid.png"
)

grid.save(
    result["curve"],
    r"artifacts/debug_regions/5_curve.png"
)

print("Done")