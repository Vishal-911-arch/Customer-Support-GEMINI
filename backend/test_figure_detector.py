from rag.figure_detector import FigureDetector

detector = FigureDetector()

figures = detector.detect("Basic_Aerodynamics")

print("\n" + "=" * 60)
print("DETECTED FIGURES")
print("=" * 60)

for figure in figures:

    print()

    print("Figure   :", figure["figure"])
    print("Title    :", figure["title"])
    print("Page     :", figure["page"])
    print("BBox     :", figure["bbox"])
    print("Document :", figure["document"])