# main.py

import os

from src.docx_processor import DocxProcessor
from src.openai_api import OpenAIAPI
from src.pdf_processor import PdfProcessor
from src.pptx_processor import PptxProcessor


def main():
    # Define your custom prompt
    prompt = (
        "You are a professional translator. Translate the following text to Slovak. "
        "Preserve the original formatting, style, and context. Do not include any additional comments."
    )
    # Input and output directories
    input_dir = "input"
    output_dir = "output"

    # List of specific files to process
    documents_to_process = ['Aria.docx']  # Specify your files here
    # documents_to_process = ['04-2023.pdf']
    # documents_to_process = ['NDT vt kutovy zvar.pptx']

    # Initialize OpenAI API
    openai_api = OpenAIAPI()

    # Process each specified file
    for file_name in documents_to_process:
        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, file_name)

        if not os.path.exists(input_path):
            print(f"File not found: {file_name}")
            continue

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
        processor.process()
        print(f"Finished processing {file_name}.\n")


if __name__ == "__main__":
    main()
