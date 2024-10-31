# main.py

import os
from src.docx_processor import DocxProcessor
from src.openai_api import OpenAIAPI
from src.pdf_processor import PdfProcessor
from src.pptx_processor import PptxProcessor


def load_prompt(prompt_file):
    """
    Load the prompt from a text file.
    """
    try:
        with open(prompt_file, "r", encoding="utf-8") as file:
            prompt = file.read().strip()
            return prompt
    except FileNotFoundError:
        print(
            f"Prompt file '{prompt_file}' not found. Please add a prompt.txt file to the input directory."
        )
        return None


def main():
    # Directories
    input_dir = "input"
    output_dir = "output"
    prompt_file = os.path.join(input_dir, "prompt.txt")

    # Load the custom prompt from prompt.txt
    prompt = load_prompt(prompt_file)
    if prompt is None:
        print("Exiting program. Prompt file is required.")
        return

    # Options to process all files or specific types
    process_all_files = False  # Set to True to process all files
    file_extension_filter = None  # e.g., ".pdf", ".docx", ".pptx" or None

    # Determine which files to process
    if process_all_files:
        documents_to_process = os.listdir(input_dir)
        if file_extension_filter:
            documents_to_process = [
                f
                for f in documents_to_process
                if f.lower().endswith(file_extension_filter)
            ]
    else:
        # List of specific files to process
        documents_to_process = [
            "Všeobecná časť + korózia skriptá.docx"
        ]  # Specify your files here

    # Initialize OpenAI API
    openai_api = OpenAIAPI(model="gpt-4-turbo")  # You can change the model here

    # Process each specified file
    for file_name in documents_to_process:
        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, file_name)

        if not os.path.exists(input_path):
            print(f"File not found: {file_name}")
            continue

        # Select the correct processor based on file type
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
