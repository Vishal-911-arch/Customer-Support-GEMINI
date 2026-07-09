from rag.ocr_document_builder import OCRDocumentBuilder

builder = OCRDocumentBuilder()

docs = builder.load_all_documents()

print()

print(f"Total Documents : {len(docs)}")

if docs:

    print("\nFirst OCR Document\n")

    print(docs[0].page_content[:500])

    print()

    print(docs[0].metadata)

else:

    print("\nNo OCR documents found.")