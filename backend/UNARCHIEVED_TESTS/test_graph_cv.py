import cv2

from rag.graph_cv import GraphCV

image = cv2.imread(
    "artifacts/graph_analysis/Basic_Aerodynamics_page_17.png"
)

cv = GraphCV()

processed = cv.preprocess(image)

cv.save_debug(
    processed["vision"],
    "graph_vision.png"
)

cv.save_debug(
    processed["ocr"],
    "graph_ocr.png"
)

print("Done")