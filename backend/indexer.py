from pathlib import Path
import os
import tempfile

import fitz
from google import genai
from langchain_core.documents import Document

from rag.context_linker import ContextLinker
from rag.loader import PDFLoader
from rag.chunker import DocumentChunker
from rag.embeddings import EmbeddingGenerator
from rag.vectordb import VectorDatabase

from utils.upload_status import upload_status
from config import (
    DOCUMENTS_DIR,
    GEMINI_API_KEY,
    GEMINI_MODEL,
)


class KnowledgeIndexer:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured.")

        self.gemini_client = genai.Client(api_key=GEMINI_API_KEY)

        self.context_linker = ContextLinker()
        self.loader = PDFLoader()
        self.chunker = DocumentChunker()
        self.embedder = EmbeddingGenerator()
        self.db = VectorDatabase()

    # ==========================================================
    # GEMINI OCR FALLBACK
    # ==========================================================

    def _ocr_pdf_with_gemini(self, pdf_path: Path):
        """
        Render each page to an image and ask Gemini to extract text.
        This is the fallback for scanned/image-only PDFs.
        """
        pdf_path = Path(pdf_path)
        document_name = pdf_path.stem
        extracted_docs = []

        pdf = fitz.open(str(pdf_path))
        try:
            total_pages = pdf.page_count

            for page_index in range(total_pages):
                page_no = page_index + 1

                upload_status["stage"] = (
                    f"🤖 Gemini OCR on page {page_no}/{total_pages}..."
                )
                upload_status["progress"] = 20 + int((page_index / max(total_pages, 1)) * 55)

                page = pdf.load_page(page_index)
                pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)

                temp_image_path = None
                try:
                    with tempfile.NamedTemporaryFile(
                        suffix=f"_page_{page_no}.png",
                        delete=False
                    ) as tmp:
                        temp_image_path = tmp.name

                    pix.save(temp_image_path)

                    uploaded = self.gemini_client.files.upload(file=temp_image_path)

                    prompt = """
Extract all readable text from this page exactly as written.
Preserve line breaks.
Do not summarize.
Do not explain.
If no readable text is present, return an empty string.
""".strip()

                    response = self.gemini_client.models.generate_content(
                        model=GEMINI_MODEL,
                        contents=[uploaded, prompt]
                    )

                    page_text = (response.text or "").strip()

                    if not page_text:
                        page_text = f"[No readable text found on page {page_no}]"

                except Exception as e:
                    print(f"Gemini OCR failed on page {page_no}: {e}")
                    page_text = f"[OCR failed on page {page_no}]"

                finally:
                    if temp_image_path and os.path.exists(temp_image_path):
                        try:
                            os.remove(temp_image_path)
                        except Exception:
                            pass

                extracted_docs.append(
                    Document(
                        page_content=page_text,
                        metadata={
                            "filename": pdf_path.name,
                            "document": document_name,
                            "page": page_no,
                            "type": "ocr_gemini",
                        },
                    )
                )

        finally:
            pdf.close()

        return extracted_docs

    # ==========================================================
    # BUILD DOCUMENTS
    # ==========================================================

    def build_multimodal_documents(self, pdf_path, include_multimodal=False):
        pdf_path = Path(pdf_path)
        document_name = pdf_path.stem

        print("\n" + "=" * 60)
        print("BUILDING DOCUMENTS")
        print("=" * 60)

        upload_status["stage"] = "📑 Extracting text from PDF..."
        upload_status["progress"] = 20

        print("\nLoading PDF Text...")

        try:
            text_docs = self.loader.load_pdf(pdf_path)
        except Exception as e:
            print("PDF text extraction failed:", e)
            text_docs = []

        print(f"Text Pages : {len(text_docs)}")

        # If readable text exists, use it directly.
        if text_docs:
            print("Native PDF text found; skipping OCR fallback.")
            return text_docs

        # If no text exists, use Gemini OCR fallback so upload still works.
        print("No extractable text found. Falling back to Gemini OCR...")

        upload_status["stage"] = "🤖 Running Gemini OCR fallback..."
        upload_status["progress"] = 35

        ocr_docs = self._ocr_pdf_with_gemini(pdf_path)

        if not ocr_docs:
            # Very rare: still keep upload from crashing.
            ocr_docs = [
                Document(
                    page_content=(
                        "This PDF was uploaded successfully, but no readable text "
                        "could be extracted from it."
                    ),
                    metadata={
                        "filename": pdf_path.name,
                        "document": document_name,
                        "page": 1,
                        "type": "pdf_stub",
                    },
                )
            ]

        print(f"OCR Pages : {len(ocr_docs)}")
        return ocr_docs

    # ==========================================================
    # INDEX DOCUMENTS
    # ==========================================================

    def _index_documents(self, documents):
        if not documents:
            raise ValueError("No text could be extracted from this PDF.")

        upload_status["stage"] = "✂️ Chunking documents..."
        upload_status["progress"] = 75

        print("\nChunking...")

        chunks = self.chunker.chunk_documents(documents)

        print(f"Created {len(chunks)} chunks")

        if not chunks:
            raise ValueError("No chunks were created from the PDF.")

        upload_status["stage"] = "🔗 Linking multimodal context..."
        upload_status["progress"] = 80

        print("\nLinking multimodal context...")

        chunks = self.context_linker.link(chunks)

        upload_status["stage"] = "🧠 Generating embeddings..."
        upload_status["progress"] = 90

        print("\nGenerating embeddings...")

        embeddings = self.embedder.embed_documents(chunks)

        upload_status["stage"] = "💾 Updating vector database..."
        upload_status["progress"] = 95

        print("\nUpdating ChromaDB...")

        self.db.add_documents(chunks, embeddings)

        upload_status["stage"] = "✅ PDF indexed successfully."
        upload_status["progress"] = 100

        print("\nIndex Complete.\n")

        return {
            "documents": len(documents),
            "chunks": len(chunks),
            "embeddings": len(embeddings),
        }

    # ==========================================================
    # INDEX SINGLE PDF
    # ==========================================================

    def index_file(self, pdf_path, include_multimodal=False):
        print("=" * 60)
        print("INDEXING NEW DOCUMENT")
        print("=" * 60)

        documents = self.build_multimodal_documents(
            pdf_path,
            include_multimodal=include_multimodal
        )

        return self._index_documents(documents)

    # ==========================================================
    # INDEX ENTIRE DIRECTORY
    # ==========================================================

    def index_directory(self, directory=DOCUMENTS_DIR):
        directory = Path(directory)

        pdf_files = sorted(directory.rglob("*.pdf"))

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