# tests/test_conversion.py

import os
from pdf2docx import Converter

def test_pdf_to_docx_conversion():
    # Define input and output paths
    input_dir = "../input"
    output_dir = "../output"
    test_pdf = "04-2023.pdf"  # Make sure this PDF exists in the input directory
    input_pdf_path = os.path.join(input_dir, test_pdf)
    output_docx_path = os.path.join(output_dir, test_pdf.replace(".pdf", ".docx"))

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Check if input PDF exists
    assert os.path.exists(input_pdf_path), f"Test PDF not found: {input_pdf_path}"

    # Convert PDF to DOCX
    try:
        converter = Converter(input_pdf_path)
        converter.convert(output_docx_path)
        converter.close()
        assert os.path.exists(output_docx_path), "DOCX file was not created."
        print(f"Conversion successful. DOCX saved to: {output_docx_path}")
    except Exception as e:
        assert False, f"Conversion failed with error: {e}"