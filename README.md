# GPT File Translator

This project leverages OpenAI’s API to translate documents while preserving the original formatting, including images, tables, fonts, and styles. It supports .pdf, .docx, and .pptx files, converting documents as necessary for consistent, high-quality translation results.

## Table of Contents

	1.	Features
	2.	Requirements
	3.	Installation
	4.	Project Structure
	5.	Usage
	6.	Supported Models
	7.	Example
	8.	Troubleshooting

## Features

	•	Format Preservation: Translates documents while keeping original formatting, including images and tables.
	•	Supports Multiple File Types: Handles .pdf, .docx, and .pptx files.
	•	Batch Processing: Processes multiple files from the input directory.
	•	Customizable Translation Prompts: Allows the user to specify custom translation prompts via prompt.txt.
	•	Pricing Calculation: Estimates the cost of each translation based on OpenAI model pricing.

## Requirements

	•	Python 3.8+
	•	OpenAI API Key (stored in .env file)
	•	LibreOffice (for DOCX to PDF conversion)
	•	Required Python packages (see Installation for instructions)

## Installation

	1.	Clone the repository:
```bash
git clone https://github.com/your-username/gpt-file-translator.git
cd gpt-file-translator
```

	2.	Set up the virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

	3.	Install dependencies:
```bash
pip install -r requirements.txt
```

	4.	Configure OpenAI API Key:
	•	Create a .env file in the root directory and add your OpenAI API key:
```bash
echo "OPENAI_API_KEY=your_openai_api_key" > .env
```

	5.	Install LibreOffice:
	•	LibreOffice is required for PDF conversions back to DOCX. Install it and ensure it’s accessible in your PATH.

## Project Structure
```
GPT_file_translator/
├── input/                   # Directory for input files
├── output/                  # Directory for output files
├── main.py                  # Main script to run translations
├── requirements.txt         # Project dependencies
├── prompt.txt               # Custom prompt file for translation instructions
├── src/                     # Source folder for processing modules
│   ├── pdf_processor.py     # PDF handling and conversion to DOCX
│   ├── docx_processor.py    # DOCX translation processing
│   ├── pptx_processor.py    # PPTX translation processing
│   ├── openai_api.py        # OpenAI API wrapper for handling requests
│   ├── utils.py             # Utility functions for chunking text
├── tests/                   # Test files for conversion and functionality
└── README.md                # Project documentation
```
## Usage

1. Prepare Input Files

	•	Place all documents for translation in the input directory.
	•	Supported formats include .pdf, .docx, and .pptx.

2. Set Custom Prompt

	•	Edit prompt.txt in the input directory to customize translation instructions.
	•	Example prompt: "Translate this document to Slovak. Maintain technical terms and formatting."

3. Run the Translator

	•	Use the following command to start translation:

python main.py


	•	Arguments (optional):
	•	process_all_files: Set to True to process all files in the input folder.
	•	file_extension_filter: Filter by file type, e.g., only process .pdf files.

4. Review Output Files

	•	Translated files will appear in the output directory, preserving original formatting.

## Supported Models

Specify the desired OpenAI model in main.py by setting:
```
openai_api = OpenAIAPI(model="gpt-4o")
```
## Available Models

	•	gpt-4o: Optimal for high-accuracy translations with a balanced cost.
	•	gpt-4-turbo: Faster, with a slight reduction in translation accuracy.
	•	gpt-4: More expensive, ideal for highly accurate translations.

Refer to OpenAI’s pricing page for the latest costs.

## Pricing Rates

These are the per-token costs used in estimating prices:

	•	GPT-4o:
	•	Input: $0.00250 / 1K tokens
	•	Output: $0.01000 / 1K tokens
	•	GPT-4 Turbo:
	•	Input: $0.0100 / 1K tokens
	•	Output: $0.0300 / 1K tokens

Example

	1.	Input Files:
	•	Place sample.pdf and sample.docx in the input directory.
	2.	Prompt:
	•	Edit prompt.txt with your desired instructions:
```
Translate this document to English. Ensure technical terminology is accurately preserved.
```

	3.	Run Translation:
```bash
python main.py
```

	4.	Output:
	•	The translated files sample.pdf and sample.docx will appear in the output directory.

## Troubleshooting

	•	LibreOffice Not Found:
	•	Ensure LibreOffice is installed and accessible from your PATH for PDF to DOCX conversions.
	•	Formatting Issues:
	•	Minor formatting discrepancies may occur, especially with complex layouts. For best results, use DOCX files.
	•	Translation Errors:
	•	Ensure prompt clarity and adjust chunk sizes in utils.py if context loss occurs.

## Additional Information

This project is a work in progress. For support, please reach out or submit an issue.