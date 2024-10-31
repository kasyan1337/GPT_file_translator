# src/pdf_processor.py

import fitz  # PyMuPDF
from src.document_processor import DocumentProcessor
from src.utils import chunk_text
from tqdm import tqdm


class PdfProcessor(DocumentProcessor):
    def process(self):
        doc = fitz.open(self.file_path)
        total_pages = len(doc)
        total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

        for page_num in tqdm(range(total_pages), desc="Translating PDF"):
            page = doc[page_num]
            original_text = page.get_text("text")
            if original_text.strip():
                # Combine text into one chunk per page to reduce API calls
                translated_text = self.openai_api.translate_text(
                    self.prompt, original_text
                )
                if translated_text:
                    # Remove existing text
                    page.clean_contents()
                    # Create a new text box with the translated text
                    rect = page.rect
                    page.insert_textbox(
                        rect, translated_text, fontsize=12, fontname="helv"
                    )
                    # Update token usage
                    usage = self.openai_api.last_usage
                    total_usage["prompt_tokens"] += usage["prompt_tokens"]
                    total_usage["completion_tokens"] += usage["completion_tokens"]
                    total_usage["total_tokens"] += usage["total_tokens"]
        doc.save(self.output_path)

        # Print token usage for the file
        print(f"Token usage for {self.file_path}: {total_usage}")
        estimated_cost = self.openai_api.calculate_cost(total_usage)
        print(f"Estimated cost for {self.file_path}: ${estimated_cost:.4f}")
