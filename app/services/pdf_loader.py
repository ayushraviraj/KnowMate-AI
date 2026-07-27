from pathlib import Path

import fitz
from langchain_core.documents import Document


class PDFLoader:
    """
    Load a PDF file using PyMuPDF.
    Each page becomes a LangChain Document.
    """

    def load(self, pdf_path: str):

        pdf = fitz.open(pdf_path)

        documents = []

        for page_number, page in enumerate(pdf, start=1):

            text = page.get_text("text")

            # Debug (remove later)
            if page_number == 1:
                print("=" * 80)
                print("PAGE 1")
                print(text)
                print("=" * 80)

            if text.strip():

                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": Path(pdf_path).name,
                            "page": page_number,
                        },
                    )
                )

        pdf.close()

        return documents