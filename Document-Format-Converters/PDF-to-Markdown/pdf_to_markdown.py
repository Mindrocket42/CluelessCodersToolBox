#!/usr/bin/env python3

# Run file and provide the path to your PDF. The PDF will be converted and saved as Markdown

import os
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

# Tell pytesseract where the tesseract.exe is located
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def pdf_to_markdown(pdf_path, md_path):
    """
    Converts a PDF file to Markdown.
    If a PDF page has text, the text is extracted.
    If the page is likely scanned (i.e., no text is found),
    OCR is performed on that page.
    """
    markdown_lines = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            extracted_text = page.extract_text()

            if extracted_text and extracted_text.strip():
                # If text is found, store it as is
                markdown_lines.append(f"## Page {page_number}\n")
                markdown_lines.append(extracted_text.strip() + "\n")
            else:
                # If no text detected, use OCR
                markdown_lines.append(f"## Page {page_number}\n")

                # Convert page to image for OCR
                images = convert_from_path(
                    pdf_path, 
                    dpi=300, 
                    first_page=page_number, 
                    last_page=page_number
                )
                if images:
                    img = images[0]
                    ocr_text = pytesseract.image_to_string(img)
                    markdown_lines.append(ocr_text.strip() + "\n")
                else:
                    markdown_lines.append("[ERROR] Unable to convert PDF page to image.\n")
    
    # Write everything to the Markdown file
    with open(md_path, 'w', encoding='utf-8') as md_file:
        md_file.write("\n".join(markdown_lines))

def main():
    pdf_path = input("Enter the full path to the PDF file: ").strip()
    if not pdf_path or not os.path.isfile(pdf_path):
        print("Invalid file path. Exiting...")
        return

    base_name, _ = os.path.splitext(pdf_path)
    md_path = base_name + ".md"

    print(f"Converting '{pdf_path}' to Markdown...")
    pdf_to_markdown(pdf_path, md_path)
    print(f"Markdown file saved to '{md_path}'")

if __name__ == "__main__":
    main()