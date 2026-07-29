from pathlib import Path

from rag.context_linker import ContextLinker
from rag.loader import PDFLoader
from rag.chunker import DocumentChunker
from rag.embeddings import EmbeddingGenerator
from rag.vectordb import VectorDatabase
from rag.page_renderer import PDFPageRenderer


from utils.upload_status import upload_status

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


    # ==========================================================
    # BUILD MULTIMODAL DOCUMENTS
    # ==========================================================

    def build_multimodal_documents(self, pdf_path, include_multimodal=False):

        if include_multimodal:
            if self.renderer is None:
                from rag.page_renderer import PDFPageRenderer
                from rag.image_classifier import ImageClassifier
                from rag.ocr import OCRProcessor
                from rag.ocr_document_builder import OCRDocumentBuilder
                from rag.figure_indexer import FigureIndexer

                self.renderer = PDFPageRenderer()
                self.image_classifier = ImageClassifier()
                self.ocr = OCRProcessor()
                self.ocr_builder = OCRDocumentBuilder()
                self.figure_indexer = FigureIndexer()

        pdf_path = Path(pdf_path)

        document_name = pdf_path.stem

        print("\n" + "=" * 60)
        print("BUILDING MULTIMODAL DOCUMENTS")
        print("=" * 60)

        # --------------------------------------------------
        # TEXT EXTRACTION
        # --------------------------------------------------

        upload_status["stage"] = (
            "📑 Extracting text from PDF..."
        )
        upload_status["progress"] = 20

        print("\nLoading PDF Text...")

        text_docs = self.loader.load_pdf(
            pdf_path
        )

        print(
            f"Text Pages : {len(text_docs)}"
        )

        # PDFs with a native text layer can be indexed immediately. Rendering,
        # image classification, and OCR duplicate that content and dominate
        # upload time, so only use them for scans or explicit enrichment.
        if text_docs and not include_multimodal:
            print("Native PDF text found; skipping page rendering and OCR.")
            return text_docs

        # --------------------------------------------------
        # PAGE RENDERING
        # --------------------------------------------------

        upload_status["stage"] = (
            "🖼 Rendering PDF pages..."
        )
        upload_status["progress"] = 30

        print("\nRendering PDF Pages...")

        self.renderer.render_pdf(
            pdf_path
        )

        # --------------------------------------------------
        # IMAGE CLASSIFICATION
        # --------------------------------------------------

        upload_status["stage"] = (
            "🔍 Detecting figures and images..."
        )
        upload_status["progress"] = 40

        # Figure indexing is currently disabled, so classification has no
        # effect on search results. Skip this costly pass for OCR fallbacks.

        # --------------------------------------------------
        # OCR
        # --------------------------------------------------

        upload_status["stage"] = (
            "📝 Running OCR..."
        )
        upload_status["progress"] = 50

        print("\nRunning OCR...")

        self.ocr.process_directory(
            RENDERED_PAGES_DIR /
            document_name
        )

        # --------------------------------------------------
        # OCR DOCUMENTS
        # --------------------------------------------------

        upload_status["stage"] = (
            "📚 Building multimodal documents..."
        )
        upload_status["progress"] = 60

        print(
            "\nLoading OCR Documents..."
        )

        ocr_docs = (
            self.ocr_builder.load_document(
                document_name
            )
        )

        print(
            f"OCR Pages : {len(ocr_docs)}"
        )

        # --------------------------------------------------
        # FIGURE INDEX
        # --------------------------------------------------

        """
        upload_status["stage"] = (
            "📊 Building Figure Index..."
        )
        upload_status["progress"] = 65

        self.figure_indexer.build_and_save(
            document_name
        )
        """

        print(
            "\nSkipping Figure Index (temporary)..."
        )

        # --------------------------------------------------
        # MERGE
        # --------------------------------------------------

        upload_status["stage"] = (
            "🔗 Merging text and OCR data..."
        )
        upload_status["progress"] = 68

        documents = (
            text_docs +
            ocr_docs
        )

        print(
            f"\nTotal Documents : {len(documents)}"
        )

        return documents

    # ==========================================================
    # INDEX DOCUMENTS
    # ==========================================================

    def _index_documents(self, documents):

        upload_status["stage"] = (
            "✂️ Chunking documents..."
        )
        upload_status["progress"] = 75

        print("\nChunking...")

        chunks = self.chunker.chunk_documents(
            documents
        )

        print(
            f"Created {len(chunks)} chunks"
        )

        # --------------------------------------------------

        upload_status["stage"] = (
            "🔗 Linking multimodal context..."
        )
        upload_status["progress"] = 80

        print(
            "\nLinking multimodal context..."
        )

        chunks = self.context_linker.link(
            chunks
        )

        # --------------------------------------------------

        upload_status["stage"] = (
            "🧠 Generating embeddings..."
        )
        upload_status["progress"] = 90

        print(
            "\nGenerating embeddings..."
        )

        embeddings = (
            self.embedder.embed_documents(
                chunks
            )
        )

        # --------------------------------------------------

        upload_status["stage"] = (
            "💾 Updating vector database..."
        )
        upload_status["progress"] = 95

        print(
            "\nUpdating ChromaDB..."
        )

        self.db.add_documents(
            chunks,
            embeddings
        )

        upload_status["stage"] = (
            "✅ PDF indexed successfully."
        )

        upload_status["progress"] = 100

        print("\nIndex Complete.\n")

        return {

            "documents":
                len(documents),

            "chunks":
                len(chunks),

            "embeddings":
                len(embeddings)

        }

    # ==========================================================
    # INDEX SINGLE PDF
    # ==========================================================

    def index_file(self, pdf_path, include_multimodal=False):

        print("=" * 60)
        print("INDEXING NEW DOCUMENT")
        print("=" * 60)

        documents = (
            self.build_multimodal_documents(
                pdf_path,
                include_multimodal=include_multimodal
            )
        )

        return self._index_documents(
            documents
        )

    # ==========================================================
    # INDEX ENTIRE DIRECTORY
    # ==========================================================

    def index_directory(
            self,
            directory=DOCUMENTS_DIR
    ):

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

            stats = self.index_file(
                pdf
            )

            total_documents += (
                stats["documents"]
            )

            total_chunks += (
                stats["chunks"]
            )

            total_embeddings += (
                stats["embeddings"]
            )

        return {

            "documents":
                total_documents,

            "chunks":
                total_chunks,

            "embeddings":
                total_embeddings

        }


if __name__ == "__main__":

    indexer = KnowledgeIndexer()

    pdf = input(
        "\nEnter PDF Path : "
    ).strip()

    stats = indexer.index_file(
        pdf
    )

    print("\n")
    print(stats)
