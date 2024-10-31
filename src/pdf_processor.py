import os
import subprocess
from src.document_processor import DocumentProcessor
from src.docx_processor import DocxProcessor
from pdf2docx import Converter
import tempfile


class PdfProcessor(DocumentProcessor):
    def process(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_docx_path = os.path.join(
                temp_dir, os.path.basename(self.file_path).replace(".pdf", ".docx")
            )
            print("Converting PDF to DOCX...")
            cv = Converter(self.file_path)
            cv.convert(temp_docx_path)
            cv.close()

            print("Processing DOCX file...")
            docx_processor = DocxProcessor(
                temp_docx_path, temp_docx_path, self.openai_api, self.prompt
            )
            docx_processor.process()

            # Print token usage
            total_usage = docx_processor.total_usage
            print(f"Token usage for {self.file_path}: {total_usage}")
            estimated_cost = self.openai_api.calculate_cost(total_usage)
            print(f"Estimated cost for {self.file_path}: ${estimated_cost:.4f}")

            # Convert DOCX back to PDF using LibreOffice
            output_pdf_dir = os.path.dirname(self.output_path)  # Just the directory
            print("Converting DOCX back to PDF using LibreOffice...")
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

            # Move the converted file to the specified output path
            final_output_path = os.path.join(
                output_pdf_dir,
                os.path.basename(temp_docx_path).replace(".docx", ".pdf"),
            )
            if os.path.exists(final_output_path):
                os.rename(final_output_path, self.output_path)
