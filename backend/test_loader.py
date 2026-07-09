from rag.loader import PDFLoader

loader = PDFLoader()

documents = loader.load_all_pdfs("documents")

print(f"Loaded {len(documents)} pages\n")

for doc in documents:
    print("=" * 50)
    print("Filename :", doc.metadata["filename"])
    print("Page     :", doc.metadata["page"])
    print(doc.page_content[:200])