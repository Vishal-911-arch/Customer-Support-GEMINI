from rag.graph_digitizer import GraphDigitizer

IMAGE = r"artifacts/debug_regions/plot.png"

digitizer = GraphDigitizer()

result = digitizer.digitize(IMAGE)

print()

print("Curves found:", result["curve_count"])

for curve in result["curves"]:

    print()

    print("Curve", curve["id"])

    print("Points:", len(curve["points"]))

    print("First 10 points:")

    print(curve["points"][:10])