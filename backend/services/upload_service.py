import shutil
from pathlib import Path

from config import (
    UPLOADED_DOCUMENTS_DIR,
    UPLOADED_IMAGES_DIR
)

from indexer import KnowledgeIndexer

from rag.graph_pipeline import GraphPipeline

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

    # ==========================================================
    # Upload PDF
    # ==========================================================

    @staticmethod
    async def upload_pdf(file):

        suffix = Path(file.filename).suffix.lower()

        if suffix not in UploadService.PDF_EXTENSIONS:

            raise ValueError(
                "Only PDF files are supported."
            )

        UPLOADED_DOCUMENTS_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        destination = (
            UPLOADED_DOCUMENTS_DIR /
            file.filename
        )

        with destination.open("wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # -------------------------------------
        # Duplicate Detection
        # -------------------------------------

        file_hash = FileHasher.sha256(destination)

        if FileRegistry.contains(file_hash):

            destination.unlink()

            return {

                "success": False,

                "message":
                "This PDF is already indexed."

            }

        # -------------------------------------
        # Knowledge Indexing
        # -------------------------------------

        indexer = KnowledgeIndexer()

        stats = indexer.index_file(destination)

        FileRegistry.add(file_hash)

        return {

            "success": True,

            "type": "pdf",

            "filename": file.filename,

            "pages": stats["pages"],

            "chunks": stats["chunks"],

            "embeddings": stats["embeddings"],

            "message":
            "PDF indexed successfully."

        }

    # ==========================================================
    # Upload Image
    # ==========================================================

    @staticmethod
    async def upload_image(file):

        suffix = Path(file.filename).suffix.lower()

        if suffix not in UploadService.IMAGE_EXTENSIONS:

            raise ValueError(
                "Unsupported image format."
            )

        UPLOADED_IMAGES_DIR.mkdir(

            parents=True,

            exist_ok=True

        )

        destination = (

            UPLOADED_IMAGES_DIR /

            file.filename

        )

        with destination.open("wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # -------------------------------------
        # Duplicate Detection
        # -------------------------------------

        file_hash = FileHasher.sha256(destination)

        if FileRegistry.contains(file_hash):

            destination.unlink()

            return {

                "success": False,

                "message":
                "This image has already been indexed."

            }

        # -------------------------------------
        # Graph Pipeline
        # -------------------------------------

        graph = GraphPipeline().analyze(

            image_path=str(destination),

            document=Path(file.filename).stem,

            page=1

            )

        FileRegistry.add(file_hash)

        return {

            "success": True,

            "type": "image",

            "filename": file.filename,

            "title": graph.get("title", ""),

            "domain": graph.get(
                "engineering_domain",
                ""
            ),

            "curve_count": graph.get(
                "curve_count",
                0
            ),

            "message":
            "Image indexed successfully."

        }