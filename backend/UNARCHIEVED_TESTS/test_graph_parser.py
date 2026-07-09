from rag.graph_cv import GraphCV
from rag.graph_ocr import GraphOCR
from rag.graph_parser import GraphParser

IMAGE = r"artifacts/graph_analysis/Basic_Aerodynamics_page_17.png"

cv = GraphCV()
ocr = GraphOCR()
parser = GraphParser()

cv_data = cv.analyze(IMAGE)

ocr_data = ocr.extract(IMAGE)

graph = parser.parse(
    ocr_data,
    cv_data
)

import json

print(
    json.dumps(
        graph,
        indent=4
    )
)