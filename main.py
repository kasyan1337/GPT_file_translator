# main.py

import os
import asyncio
from src.openai_api import OpenAIAPI
from src.docx_processor import DocxProcessor
from src.pptx_processor import PptxProcessor
from src.pdf_processor import PdfProcessor


async def main():
    # Define your custom prompt
    prompt = "Translate the following text to Slovak while preserving the original formatting."

    # Input and output directories
    input_dir = "input"
    output_dir = "output"

    # Get list of files to process
    files_to_process = os.listdir(input_dir)

    # Initialize OpenAI API
    openai_api = OpenAIAPI()

    # Process each file
    tasks = []

    for file_name in files_to_process:
        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, file_name)

        if file_name.lower().endswith(".docx"):
            processor = DocxProcessor(input_path, output_path, openai_api, prompt)
        elif file_name.lower().endswith(".pptx"):
            processor = PptxProcessor(input_path, output_path, openai_api, prompt)
        elif file_name.lower().endswith(".pdf"):
            processor = PdfProcessor(input_path, output_path, openai_api, prompt)
        else:
            print(f"Unsupported file type: {file_name}")
            continue

        print(f"Processing {file_name}...")
        tasks.append(processor.process())

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
