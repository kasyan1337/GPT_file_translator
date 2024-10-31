# src/pptx_processor.py

from pptx import Presentation
from src.document_processor import DocumentProcessor

class PptxProcessor(DocumentProcessor):
    def process(self):
        presentation = Presentation(self.file_path)
        for slide in presentation.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    original_text = shape.text
                    if original_text.strip():
                        translated_text = self.openai_api.translate_text(self.prompt, original_text)
                        shape.text = translated_text
        presentation.save(self.output_path)