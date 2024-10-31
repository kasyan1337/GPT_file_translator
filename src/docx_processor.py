# src/docx_processor.py

import asyncio
from docx import Document
from src.document_processor import DocumentProcessor
from src.utils import chunk_text
from tqdm.asyncio import tqdm_asyncio


class DocxProcessor(DocumentProcessor):
    async def process(self):
        document = Document(self.file_path)
        tasks = []

        for paragraph in document.paragraphs:
            original_text = paragraph.text
            if original_text.strip():
                chunks = chunk_text(original_text)
                tasks.extend(
                    [self.translate_chunk(chunk, paragraph) for chunk in chunks]
                )

        await tqdm_asyncio.gather(*tasks, desc="Translating DOCX")

        document.save(self.output_path)

    async def translate_chunk(self, text, paragraph):
        translated_text = await self.openai_api.translate_text(self.prompt, text)
        if translated_text:
            paragraph.text = translated_text
