from pathlib import Path
import fitz


class KnowledgeService:

    def __init__(self):

        self.documents = (
            Path(__file__).resolve().parent.parent
            / "documents"
        )

    # ====================================================
    # GET PDF INFORMATION
    # ====================================================

    def get_pdf_info(self, folder):

        path = self.documents / folder

        if not path.exists():

            return []

        pdfs = []

        for file in sorted(path.glob("*.pdf")):

            try:

                doc = fitz.open(file)

                pdfs.append({

                    "name": file.stem,

                    "filename": file.name,

                    "pages": len(doc)

                })

                doc.close()

            except Exception:

                continue

        return pdfs

    # ====================================================
    # GET IMAGE INFORMATION
    # ====================================================

    def get_images(self):

        path = self.documents / "images"

        if not path.exists():

            return []

        images = []

        extensions = {

            ".png",

            ".jpg",

            ".jpeg",

            ".bmp",

            ".webp"

        }

        for file in sorted(path.iterdir()):

            if file.suffix.lower() in extensions:

                images.append({

                    "name": file.stem,

                    "filename": file.name

                })

        return images

    # ====================================================
    # GET UPLOADED FILES
    # ====================================================

    def get_uploaded(self):

        path = self.documents / "uploaded"

        if not path.exists():

            return []

        uploaded = []

        for file in sorted(path.iterdir()):

            uploaded.append({

                "name": file.stem,

                "filename": file.name

            })

        return uploaded

    # ====================================================
    # MAIN API
    # ====================================================

    def get_knowledge(self):

        return {

            "manuals": self.get_pdf_info(

                "manuals"

            ),

            "maintenance": self.get_pdf_info(

                "maintenance"

            ),

            "safety": self.get_pdf_info(

                "safety"

            ),

            "images": self.get_images(),

            "uploaded": self.get_uploaded()

        }


knowledge_service = KnowledgeService()