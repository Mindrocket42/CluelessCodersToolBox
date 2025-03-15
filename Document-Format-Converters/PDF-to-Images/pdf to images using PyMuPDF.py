# Requires file path to be hard coded into this file +/-Line44

import fitz  # PyMuPDF
import os

def pdf_to_images(pdf_path, output_folder, image_format="png", zoom=2):
    """
    Convert each page of a PDF to an image.

    :param pdf_path: Path to the PDF file.
    :param output_folder: Folder where the images will be saved.
    :param image_format: Format of the output images (e.g., 'png', 'jpeg').
    :param zoom: Zoom factor to increase the resolution of the output images.
    """
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through each page
    for page_num in range(len(pdf_document)):
        # Get the page
        page = pdf_document.load_page(page_num)

        # Set the zoom factor
        mat = fitz.Matrix(zoom, zoom)

        # Render the page to an image (pix)
        pix = page.get_pixmap(matrix=mat, alpha=False)

        # Save the image
        image_path = os.path.join(output_folder, f"slide_{page_num + 1}.{image_format}")
        pix.save(image_path)

        print(f"Saved {image_path}")

    # Close the PDF file
    pdf_document.close()

if __name__ == "__main__":
    # Path to the PDF file
    pdf_path = r"FILE PATH"

    # Output folder where images will be saved
    output_folder = "output_images"

    # Convert PDF to images
    pdf_to_images(pdf_path, output_folder)
