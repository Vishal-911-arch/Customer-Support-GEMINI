from config import RENDERED_PAGES_DIR
from rag.ocr import OCRProcessor

ocr = OCRProcessor()

results = ocr.process_directory(
    RENDERED_PAGES_DIR / "Glider_Flying_Handbook"
)

print("\nFirst Page Preview:\n")

print(results[0]["text"][:1000])