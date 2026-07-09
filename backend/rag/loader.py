import os
from pathlib import Path

import fitz
from langchain_core.documents import Document


class PDFLoader:
    """
    Loads PDF files and converts each page into LangChain Documents.
    """

    def load_pdf(self, pdf_path):

        pdf_path = Path(pdf_path)

        filename = pdf_path.name

        document_name = pdf_path.stem

        documents = []

        pdf = fitz.open(str(pdf_path))

        print(f"📄 {filename}")

        for page_num in range(len(pdf)):

            page = pdf.load_page(page_num)

            text = page.get_text("text").strip()

            if not text:
                continue

            documents.append(

                Document(

                    page_content=text,

                    metadata={

                        "source": str(pdf_path),

                        "filename": filename,

                        "document": document_name,

                        "page": page_num + 1,

                        "type": "pdf"

                    }

                )

            )

        pdf.close()

        return documents

    # ---------------------------------------------------------

    def load_all_pdfs(self, folder_path):

        folder_path = Path(folder_path)

        all_documents = []

        pdf_count = 0

        print("\nScanning Knowledge Base...\n")

        for root, _, files in os.walk(folder_path):

            pdf_files = [

                f

                for f in files

                if f.lower().endswith(".pdf")

            ]

            if not pdf_files:
                continue

            category = Path(root).name

            print(f"\n📁 {category}")

            for file in pdf_files:

                pdf_path = Path(root) / file

                docs = self.load_pdf(pdf_path)

                for doc in docs:

                    doc.metadata["category"] = category

                all_documents.extend(docs)

                pdf_count += 1

        print("\n--------------------------------")

        print(f"Loaded PDFs : {pdf_count}")

        print(f"Loaded Pages: {len(all_documents)}")

        print("--------------------------------\n")

        return all_documents