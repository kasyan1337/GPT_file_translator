# src/docx_processor.py

from docx import Document
from src.document_processor import DocumentProcessor

class DocxProcessor(DocumentProcessor):
    def process(self):
        document = Document(self.file_path)
        for paragraph in document.paragraphs:
            original_text = paragraph.text
            if original_text.strip():
                translated_text = self.openai_api.translate_text(self.prompt, original_text)
                paragraph.text = translated_text
        document.save(self.output_path)