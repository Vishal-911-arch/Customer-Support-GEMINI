import json
from pathlib import Path

from langchain_core.documents import Document

from config import OCR_OUTPUT_DIR


class OCRDocumentBuilder:
    """
    Builds LangChain Documents from OCR JSON files.

    Folder Structure

    artifacts/
        ocr_output/
            Document/
                page_1.json
                page_2.json
    """

    def __init__(self):

        self.ocr_root = Path(OCR_OUTPUT_DIR)

    # ---------------------------------------------------------

    def load_document(self, document_name):

        document_folder = self.ocr_root / document_name

        if not document_folder.exists():

            print(f"[WARNING] OCR folder not found : {document_folder}")

            return []

        json_files = sorted(
            document_folder.glob("*.json")
        )

        if not json_files:

            print(f"[WARNING] No OCR JSON files found.")

            return []

        documents = []

        print(f"\nLoading OCR : {document_name}")

        for json_file in json_files:

            try:

                with open(
                    json_file,
                    "r",
                    encoding="utf-8"
                ) as f:

                    data = json.load(f)

            except Exception as e:

                print(e)

                continue

            text = data.get(
                "text",
                ""
            ).strip()

            if not text:
                continue

            page_name = data.get(
                "page",
                json_file.stem
            )

            # page_12 -> 12

            if isinstance(page_name, str):

                if page_name.startswith("page_"):

                    page_number = int(
                        page_name.replace(
                            "page_",
                            ""
                        )
                    )

                else:

                    page_number = page_name

            else:

                page_number = page_name

            doc = Document(

                page_content=text,

                metadata={

                    "document": data.get(
                        "document",
                        document_name
                    ),

                    "filename":
                    f"{document_name}.pdf",

                    "page": page_number,

                    "source":
                    data.get(
                        "image_path",
                        ""
                    ),

                    "type": "ocr",

                    "word_count":
                    len(
                        data.get(
                            "words",
                            []
                        )
                    )

                }

            )

            documents.append(doc)

        print(f"Loaded {len(documents)} OCR pages")

        return documents

    # ---------------------------------------------------------

    def load_all_documents(self):

        all_docs = []

        folders = sorted(

            [

                folder

                for folder in self.ocr_root.iterdir()

                if folder.is_dir()

            ]

        )

        for folder in folders:

            docs = self.load_document(

                folder.name

            )

            all_docs.extend(docs)

        print(f"\nTotal OCR Documents : {len(all_docs)}")

        return all_docs