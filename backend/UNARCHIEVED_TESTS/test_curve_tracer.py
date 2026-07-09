from rag.curve_tracer import CurveTracer

tracer = CurveTracer()

curves = tracer.trace(
    "artifacts/debug_regions/plot.png"
)

print("Curves found :", len(curves))

for c in curves:
    print(
        c["id"],
        len(c["points"])
    )