# src/pdf_processor.py

import asyncio
import fitz  # PyMuPDF
from src.document_processor import DocumentProcessor
from src.utils import chunk_text
from tqdm.asyncio import tqdm_asyncio


class PdfProcessor(DocumentProcessor):
    async def process(self):
        doc = fitz.open(self.file_path)
        tasks = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            original_text = page.get_text()
            if original_text.strip():
                chunks = chunk_text(original_text)
                tasks.extend([self.translate_chunk(chunk, page) for chunk in chunks])

        await tqdm_asyncio.gather(*tasks, desc="Translating PDF")

        doc.save(self.output_path)

    async def translate_chunk(self, text, page):
        translated_text = await self.openai_api.translate_text(self.prompt, text)
        if translated_text:
            # Clear existing text
            page.clean_contents()
            # Add translated text
            rect = page.rect
            text_writer = fitz.TextWriter(rect)
            text_writer.append(rect.tl, translated_text)
            text_writer.write_text(page)
