from pathlib import Path
import fitz

from config import (
    RENDER_DPI,
    RENDERED_PAGES_DIR
)


class PDFPageRenderer:

    def __init__(self, dpi=RENDER_DPI):

        self.dpi = dpi

    def render_pdf(self, pdf_path):

        pdf_path = Path(pdf_path)

        document_name = pdf_path.stem

        output_dir = (
            RENDERED_PAGES_DIR /
            document_name
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        pdf = fitz.open(pdf_path)

        zoom = self.dpi / 72

        matrix = fitz.Matrix(
            zoom,
            zoom
        )

        rendered_pages = []

        for page_number in range(len(pdf)):

            page = pdf.load_page(page_number)

            pix = page.get_pixmap(
                matrix=matrix,
                alpha=False
            )

            image_path = (
                output_dir /
                f"page_{page_number+1}.png"
            )

            pix.save(image_path)

            rendered_pages.append({

                "document": document_name,

                "page": page_number + 1,

                "image_path": image_path

            })

        pdf.close()

        return rendered_pages