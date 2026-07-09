from rag.loader import PDFLoader
from rag.chunker import DocumentChunker
from rag.embeddings import EmbeddingGenerator

print("\nLoading PDFs...")

loader = PDFLoader()

documents = loader.load_all_pdfs("documents")

print(f"Loaded {len(documents)} pages")

print("\nChunking...")

chunker = DocumentChunker()

chunks = chunker.split_documents(documents)

print(f"Created {len(chunks)} chunks")

embedder = EmbeddingGenerator(batch_size=32)

embeddings = embedder.embed_documents(chunks)

print(f"\nGenerated {len(embeddings)} embeddings")

print("\nEmbedding Dimension:")

print(len(embeddings[0]))