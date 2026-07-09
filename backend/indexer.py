from rag.context_linker import ContextLinker
from rag.figure_indexer import FigureIndexer
from pathlib import Path

from rag.loader import PDFLoader
from rag.chunker import DocumentChunker
from rag.embeddings import EmbeddingGenerator
from rag.vectordb import VectorDatabase
from rag.page_renderer import PDFPageRenderer
from rag.image_classifier import ImageClassifier
from rag.ocr import OCRProcessor
from rag.ocr_document_builder import OCRDocumentBuilder

from config import (
    DOCUMENTS_DIR,
    RENDERED_PAGES_DIR,
)


class KnowledgeIndexer:

    def __init__(self):
        self.context_linker = ContextLinker()

        self.loader = PDFLoader()

        self.chunker = DocumentChunker()

        self.embedder = EmbeddingGenerator()

        self.db = VectorDatabase()

        self.renderer = PDFPageRenderer()

        self.image_classifier = ImageClassifier()

        self.ocr = OCRProcessor()

        self.ocr_builder = OCRDocumentBuilder()

        self.figure_indexer = FigureIndexer()

    # ==========================================================
    # BUILD MULTIMODAL DOCUMENTS
    # ==========================================================

    def build_multimodal_documents(self, pdf_path):

        pdf_path = Path(pdf_path)

        document_name = pdf_path.stem

        print("\n" + "=" * 60)
        print("BUILDING MULTIMODAL DOCUMENTS")
        print("=" * 60)

        # --------------------------------------------------
        # TEXT EXTRACTION
        # --------------------------------------------------

        print("\nLoading PDF Text...")

        text_docs = self.loader.load_pdf(pdf_path)

        print(f"Text Pages : {len(text_docs)}")

        # --------------------------------------------------
        # PAGE RENDERING
        # --------------------------------------------------

        print("\nRendering PDF Pages...")

        self.renderer.render_pdf(pdf_path)

        # --------------------------------------------------
        # IMAGE CLASSIFICATION
        # --------------------------------------------------

        print("\nRunning Image Classification...")

        self.image_classifier.process_document(
            document_name
        )

        # --------------------------------------------------
        # OCR
        # --------------------------------------------------

        print("\nRunning OCR...")

        self.ocr.process_directory(
            RENDERED_PAGES_DIR / document_name
        )

        # --------------------------------------------------
        # OCR DOCUMENTS
        # --------------------------------------------------

        print("\nLoading OCR Documents...")

        ocr_docs = self.ocr_builder.load_document(
            document_name
        )

        print(f"OCR Pages : {len(ocr_docs)}")
        # ----------------------------------------------------
        # FIGURE INDEX
        # ----------------------------------------------------

        '''print("\nBuilding Figure Index...")

        self.figure_indexer.build_and_save(
            document_name
)'''
        print("\nSkipping Figure Index (temporary)...")
        # --------------------------------------------------
        # MERGE
        # --------------------------------------------------

        documents = text_docs + ocr_docs

        print(f"\nTotal Documents : {len(documents)}")

        return documents

    # ==========================================================
    # INDEX DOCUMENTS
    # ==========================================================

    def _index_documents(self, documents):

        print("\nChunking...")

        chunks = self.chunker.chunk_documents(
            documents
            )

        print(f"Created {len(chunks)} chunks")

        print("\nLinking multimodal context...")

        chunks = self.context_linker.link(chunks)

        print("\nGenerating embeddings...")

        embeddings = self.embedder.embed_documents(
            chunks
        )

        
        print("\nUpdating ChromaDB...")

        self.db.add_documents(
            chunks,
            embeddings
        )

        print("\nIndex Complete.\n")

        return {
            "documents": len(documents),
            "chunks": len(chunks),
            "embeddings": len(embeddings)
        }

    # ==========================================================
    # INDEX SINGLE PDF
    # ==========================================================

    def index_file(self, pdf_path):

        print("=" * 60)
        print("INDEXING NEW DOCUMENT")
        print("=" * 60)

        documents = self.build_multimodal_documents(
            pdf_path
        )

        return self._index_documents(
            documents
        )

    # ==========================================================
    # INDEX ENTIRE KNOWLEDGE BASE
    # ==========================================================

    def index_directory(self, directory=DOCUMENTS_DIR):

        directory = Path(directory)

        pdf_files = sorted(
            directory.rglob("*.pdf")
        )

        total_documents = 0
        total_chunks = 0
        total_embeddings = 0

        for pdf in pdf_files:

            print("\n" + "#" * 70)
            print(pdf.name)
            print("#" * 70)

            stats = self.index_file(pdf)

            total_documents += stats["documents"]
            total_chunks += stats["chunks"]
            total_embeddings += stats["embeddings"]

        return {
            "documents": total_documents,
            "chunks": total_chunks,
            "embeddings": total_embeddings
        }


if __name__ == "__main__":

    indexer = KnowledgeIndexer()

    pdf = input("\nEnter PDF Path : ").strip()

    stats = indexer.index_file(pdf)

    print("\n")
    print(stats)

