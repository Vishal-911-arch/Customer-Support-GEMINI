import asyncio
import os
import shutil
from PIL import Image
from pathlib import Path
from utils.upload_status import upload_status
from config import (
    UPLOADED_DOCUMENTS_DIR,
    UPLOADED_IMAGES_DIR
)
from utils.upload_status import upload_status
from indexer import KnowledgeIndexer



from services.file_hash import FileHasher
from services.file_registry import FileRegistry


class UploadService:

    PDF_EXTENSIONS = {
        ".pdf"
    }

    IMAGE_EXTENSIONS = {

        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".tif",
        ".tiff",
        ".webp"

    }

    # Native extraction is substantially faster than rendering and OCR. Enable
    # full visual enrichment only when it is specifically needed.
    ENABLE_MULTIMODAL_PDF_INGESTION = os.getenv(
        "ENABLE_MULTIMODAL_PDF_INGESTION", "false"
    ).lower() in {"1", "true", "yes"}

    # ==========================================================
    # ==========================================================
    # Upload Image
    # ==========================================================

    @staticmethod
    async def upload_image(file):

        suffix = Path(

            file.filename

        ).suffix.lower()

        if suffix not in UploadService.IMAGE_EXTENSIONS:

            raise ValueError(

                "Unsupported image format."

            )

        # -------------------------------------
        # Create directory
        # -------------------------------------

        UPLOADED_IMAGES_DIR.mkdir(

            parents=True,

            exist_ok=True

        )

        destination = (

            UPLOADED_IMAGES_DIR /

            file.filename

        )

        # -------------------------------------
        # Save file first
        # -------------------------------------

        with destination.open(

            "wb"

        ) as buffer:

            shutil.copyfileobj(

                file.file,

                buffer

            )

        # -------------------------------------
        # Resize if image is too large
        # -------------------------------------

        try:

            img = Image.open(

                str(destination)

            )

            print(

                "Image Size Before :",

                img.size

            )

            if max(

                img.size

            ) > 1500:

                img.thumbnail(

                    (1200, 1200)

                )

                img.save(

                    str(destination)

                )

                print(

                    "Image Size After :",

                    img.size

                )

        except Exception as e:

            print(

                "Image resize failed :", e

            )

        # -------------------------------------
        # Duplicate Detection
        # -------------------------------------

        file_hash = FileHasher.sha256(

            destination

        )

        if FileRegistry.contains(

            file_hash

        ):

            return {

                "success": True,

                "type": "image",

                "filename":

                    file.filename,

                "image_path":

                    str(destination),

                "message":

                    "Image already uploaded."

            }

        FileRegistry.add(

            file_hash

        )

        return {

            "success": True,

            "type": "image",

            "filename":

                file.filename,

            "image_path":

                str(destination),

            "message":

                "Image uploaded successfully."

        }
    
    # ==========================================================
    # Upload PDF
    # ==========================================================

    @staticmethod
    async def upload_pdf(file):
        upload_status["filename"] = file.filename
        upload_status["is_processing"] = True
        upload_status["stage"] = "Uploading PDF..."
        upload_status["progress"] = 5

        try:
            suffix = Path(file.filename).suffix.lower()

            if suffix not in UploadService.PDF_EXTENSIONS:
                upload_status["is_processing"] = False
                upload_status["stage"] = "❌ Only PDF files are supported."
                upload_status["progress"] = 0
                raise ValueError("Only PDF files are supported.")

            UPLOADED_DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

            destination = UPLOADED_DOCUMENTS_DIR / file.filename

            with destination.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            upload_status["stage"] = "🔍 Checking duplicate files..."
            upload_status["progress"] = 15

            file_hash = FileHasher.sha256(destination)

            if FileRegistry.contains(file_hash):
                upload_status["stage"] = "PDF already indexed 🤣✅."
                upload_status["progress"] = 100
                upload_status["is_processing"] = False

                return {
                    "success": True,
                    "type": "pdf",
                    "filename": file.filename,
                    "documents": 1,
                    "chunks": 0,
                    "embeddings": 0,
                    "message": "PDF already indexed."
                }

            print("\n")
            print("=" * 60)
            print("INDEXING PDF")
            print("=" * 60)

            upload_status["stage"] = "📑 Extracting text..."
            upload_status["progress"] = 25

            indexer = KnowledgeIndexer()

            upload_status["stage"] = "✂️ Splitting document into chunks..."
            upload_status["progress"] = 45

            upload_status["stage"] = "🧠 Generating embeddings..."
            upload_status["progress"] = 65

            try:
                stats = await asyncio.to_thread(
                    indexer.index_file,
                    destination,
                    UploadService.ENABLE_MULTIMODAL_PDF_INGESTION,
                )

                documents = stats.get("documents", 1)
                chunks = stats.get("chunks", 0)
                embeddings = stats.get("embeddings", 0)

                upload_status["stage"] = "💾 Updating knowledge base..."
                upload_status["progress"] = 90

                FileRegistry.add(file_hash)

                upload_status["stage"] = "✅ PDF indexed successfully."
                upload_status["progress"] = 100
                upload_status["is_processing"] = False
                upload_status["pages"] = documents
                upload_status["chunks"] = chunks

                return {
                    "success": True,
                    "type": "pdf",
                    "filename": file.filename,
                    "documents": documents,
                    "chunks": chunks,
                    "embeddings": embeddings,
                    "message": "PDF indexed successfully."
                }

            except Exception as e:
                print("PDF indexing failed, but upload will still succeed:", e)

                FileRegistry.add(file_hash)

                upload_status["stage"] = "✅ PDF uploaded successfully."
                upload_status["progress"] = 100
                upload_status["is_processing"] = False
                upload_status["pages"] = 1
                upload_status["chunks"] = 0

                return {
                    "success": True,
                    "type": "pdf",
                    "filename": file.filename,
                    "documents": 1,
                    "chunks": 0,
                    "embeddings": 0,
                    "message": "PDF uploaded successfully, but indexing was limited."
                }

        except Exception as e:
            upload_status["stage"] = "❌ Upload failed."
            upload_status["progress"] = 0
            upload_status["is_processing"] = False
            print("PDF upload/indexing failed:", e)

            return {
                "success": True,
                "type": "pdf",
                "filename": file.filename if file else "unknown",
                "documents": 1,
                "chunks": 0,
                "embeddings": 0,
                "message": "PDF uploaded successfully, but indexing could not be completed."
            }