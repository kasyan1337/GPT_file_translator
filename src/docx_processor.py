# src/docx_processor.py

from docx import Document
from src.document_processor import DocumentProcessor
from tqdm import tqdm
from src.utils import chunk_paragraphs

class DocxProcessor(DocumentProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_usage = {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}

    def process(self):
        document = Document(self.file_path)

        # Collect all paragraphs with text
        paragraphs = [p for p in document.paragraphs if p.text.strip()]

        # Group paragraphs into chunks
        paragraph_chunks = chunk_paragraphs(paragraphs, max_tokens=7500, model="gpt-4-turbo")

        for chunk in tqdm(paragraph_chunks, desc="Translating DOCX"):
            original_text = "\n".join([p.text for p in chunk])
            translated_text = self.openai_api.translate_text(self.prompt, original_text)
            if translated_text:
                translated_paragraphs = translated_text.split("\n")
                for p, t in zip(chunk, translated_paragraphs):
                    p.text = t
                usage = self.openai_api.last_usage
                self.total_usage['prompt_tokens'] += usage['prompt_tokens']
                self.total_usage['completion_tokens'] += usage['completion_tokens']
                self.total_usage['total_tokens'] += usage['total_tokens']
            else:
                print("Translation failed for a chunk.")

        document.save(self.output_path)

        print(f"Token usage for {self.file_path}: {self.total_usage}")
        estimated_cost = self.openai_api.calculate_cost(self.total_usage)
        print(f"Estimated cost for {self.file_path}: ${estimated_cost:.4f}")