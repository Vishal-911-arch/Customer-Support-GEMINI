
from rag.graph_ocr import GraphOCR
from rag.graph_grid import GraphGridRemover
from rag.curve_tracer import CurveTracer
import json
import cv2
import os

IMAGE = "debug_regions/plot.png"


def main():

    print("=" * 60)
    print("GRAPH ANALYZER TEST")
    print("=" * 60)

    # ---------------------------------------------------
    # Check image
    # ---------------------------------------------------

    if not os.path.exists(IMAGE):
        print("Image not found:", IMAGE)
        return

    image = cv2.imread(IMAGE)

    print("Image shape:", image.shape)

    # ---------------------------------------------------
    # OCR
    # ---------------------------------------------------

    print("\nRunning OCR...")

    ocr = GraphOCR()

    ocr_result = ocr.extract(IMAGE)

    print(json.dumps(ocr_result, indent=4))

    # ---------------------------------------------------
    # Grid Removal
    # ---------------------------------------------------

    print("\nRemoving Grid...")

    remover = GraphGridRemover()

    clean = remover.remove_grid(IMAGE)

    cv2.imwrite("debug_regions/clean_plot.png", clean)

    print("Saved : clean_plot.png")

    # ---------------------------------------------------
    # Curve Tracing
    # ---------------------------------------------------

    print("\nTracing Curves...")

    tracer = CurveTracer()

    curves = tracer.trace(clean)

    print("Curves detected :", len(curves))

    for i, curve in enumerate(curves):
        print(f"Curve {i} : {len(curve)} points")

    # ---------------------------------------------------
    # Final Result
    # ---------------------------------------------------

    result = {
        "title": ocr_result["title"],
        "x_axis": ocr_result["x_axis"],
        "y_axis": ocr_result["y_axis"],
        "legend": ocr_result["legend"],
        "ticks": ocr_result["ticks"],
        "curves": len(curves)
    }

    print("\nFINAL OUTPUT")

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()