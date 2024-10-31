# src/pptx_processor.py

from pptx import Presentation
from src.document_processor import DocumentProcessor
from tqdm import tqdm


class PptxProcessor(DocumentProcessor):
    def process(self):
        presentation = Presentation(self.file_path)
        total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

        slides = [slide for slide in presentation.slides]
        for slide in tqdm(slides, desc="Translating PPTX"):
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    original_text = shape.text
                    translated_text = self.openai_api.translate_text(
                        self.prompt, original_text
                    )
                    if translated_text:
                        shape.text = translated_text
                        # Update token usage
                        usage = self.openai_api.last_usage
                        total_usage["prompt_tokens"] += usage["prompt_tokens"]
                        total_usage["completion_tokens"] += usage["completion_tokens"]
                        total_usage["total_tokens"] += usage["total_tokens"]

        presentation.save(self.output_path)

        # Print token usage for the file
        print(f"Token usage for {self.file_path}: {total_usage}")
        estimated_cost = self.openai_api.calculate_cost(total_usage)
        print(f"Estimated cost for {self.file_path}: ${estimated_cost:.4f}")
