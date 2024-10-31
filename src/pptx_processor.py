# src/pptx_processor.py

import asyncio
from pptx import Presentation
from src.document_processor import DocumentProcessor
from src.utils import chunk_text
from tqdm.asyncio import tqdm_asyncio


class PptxProcessor(DocumentProcessor):
    async def process(self):
        presentation = Presentation(self.file_path)
        tasks = []

        for slide in presentation.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    original_text = shape.text
                    if original_text.strip():
                        chunks = chunk_text(original_text)
                        tasks.extend(
                            [self.translate_chunk(chunk, shape) for chunk in chunks]
                        )

        await tqdm_asyncio.gather(*tasks, desc="Translating PPTX")

        presentation.save(self.output_path)

    async def translate_chunk(self, text, shape):
        translated_text = await self.openai_api.translate_text(self.prompt, text)
        if translated_text:
            shape.text = translated_text
