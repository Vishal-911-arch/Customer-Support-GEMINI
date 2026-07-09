from rag.loader import PDFLoader
from rag.chunker import DocumentChunker

loader = PDFLoader()

documents = loader.load_all_pdfs("documents")

print(f"Pages Loaded : {len(documents)}")

chunker = DocumentChunker()

chunks = chunker.split_documents(documents)

print(f"Chunks Created : {len(chunks)}")

print("\nFirst Chunk\n")
print("=" * 60)

print(chunks[0].page_content[:500])

print("\nMetadata")

print(chunks[0].metadata)