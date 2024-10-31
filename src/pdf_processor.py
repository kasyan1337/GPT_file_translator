# src/pdf_processor.py

import os
import subprocess
import tempfile

from pdf2docx import Converter

from src.document_processor import DocumentProcessor
from src.docx_processor import DocxProcessor


class PdfProcessor(DocumentProcessor):
    def process(self):
        # Create a temporary directory for intermediate files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Define paths for temporary DOCX and output PDF
            temp_docx_path = os.path.join(
                temp_dir, os.path.basename(self.file_path).replace(".pdf", ".docx")
            )

            # Step 1: Convert PDF to DOCX
            print("Converting PDF to DOCX...")
            cv = Converter(self.file_path)
            cv.convert(temp_docx_path)
            cv.close()

            # Step 2: Translate DOCX using DocxProcessor
            print("Processing DOCX file for translation...")
            docx_processor = DocxProcessor(
                temp_docx_path, temp_docx_path, self.openai_api, self.prompt
            )
            docx_processor.process()

            # Step 3: Convert Translated DOCX Back to PDF
            output_pdf_dir = os.path.dirname(self.output_path)
            print("Converting translated DOCX back to PDF...")
            subprocess.run(
                [
                    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
                    "--headless",
                    "--convert-to",
                    "pdf",
                    temp_docx_path,
                    "--outdir",
                    output_pdf_dir,
                ]
            )

            # Step 4: Rename and Move Final PDF to Output Path
            final_output_path = os.path.join(
                output_pdf_dir, os.path.basename(temp_docx_path).replace(".docx", ".pdf")
            )
            if os.path.exists(final_output_path):
                os.rename(final_output_path, self.output_path)

            print(f"PDF translation and conversion completed. Saved as: {self.output_path}")
