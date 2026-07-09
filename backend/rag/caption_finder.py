import re

from rag.ocr_document_builder import OCRDocumentBuilder


class CaptionFinder:

    def __init__(self):

        self.ocr = OCRDocumentBuilder()

    # -------------------------------------------------------

    def find_page(self, document_name, figure_number):

        docs = self.ocr.load_document(document_name)

        pattern = re.compile(

            rf"Figure\s*{re.escape(figure_number)}",

            flags=re.IGNORECASE
        )

        for page_no, page in enumerate(docs, start=1):

            if "Figure" in page.page_content:

                print("\nPAGE", page_no)
                print(page.page_content[:500])

            if pattern.search(page.page_content):

                print("\nMATCH FOUND")
                print(page.page_content)
                return page_no