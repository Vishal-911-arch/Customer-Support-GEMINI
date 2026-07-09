from rag.loader import PDFLoader
from rag.chunker import DocumentChunker
from rag.embeddings import EmbeddingGenerator
from rag.vectordb import VectorDatabase

print("Loading PDFs...")

loader = PDFLoader()

documents = loader.load_all_pdfs("documents")

print(f"Pages : {len(documents)}")

chunker = DocumentChunker()

chunks = chunker.split_documents(documents)

print(f"Chunks : {len(chunks)}")

embedder = EmbeddingGenerator()

embeddings = embedder.embed_documents(chunks)

db = VectorDatabase()

db.add_documents(
    chunks,
    embeddings
)

print()

print("Stored Chunks:")

print(db.count())