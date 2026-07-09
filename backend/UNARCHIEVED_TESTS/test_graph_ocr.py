from rag.graph_ocr import GraphOCR

ocr = GraphOCR()

result = ocr.extract(
    r"C:\Users\Vishal Sharma\Desktop\HAL-AI-Customer-Support\backend\artifacts\graph_analysis\Basic_Aerodynamics_page_17.png"
)

print()

for k, v in result.items():

    print(k)

    print(v)

    print()