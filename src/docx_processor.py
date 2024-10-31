# src/docx_processor.py

from docx import Document
from src.document_processor import DocumentProcessor
from tqdm import tqdm


class DocxProcessor(DocumentProcessor):
    def process(self):
        document = Document(self.file_path)
        total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

        paragraphs = [p for p in document.paragraphs if p.text.strip()]
        for paragraph in tqdm(paragraphs, desc="Translating DOCX"):
            original_text = paragraph.text
            translated_text = self.openai_api.translate_text(self.prompt, original_text)
            if translated_text:
                paragraph.text = translated_text
                # Update token usage
                usage = self.openai_api.last_usage
                total_usage["prompt_tokens"] += usage["prompt_tokens"]
                total_usage["completion_tokens"] += usage["completion_tokens"]
                total_usage["total_tokens"] += usage["total_tokens"]

        document.save(self.output_path)

        # Print token usage for the file
        print(f"Token usage for {self.file_path}: {total_usage}")
        estimated_cost = self.openai_api.calculate_cost(total_usage)
        print(f"Estimated cost for {self.file_path}: ${estimated_cost:.4f}")
