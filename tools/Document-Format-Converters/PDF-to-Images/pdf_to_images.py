import os
import sys
from pathlib import Path
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFPageCountError, PDFSyntaxError
import logging
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PDFConverter:
    def __init__(self, input_dir='Input-Files', output_dir='Output-Images'):
        """Initialize the PDF converter with input and output directories."""
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.dpi = 300  # High resolution for OCR
        self.fmt = 'PNG'  # PNG format for better quality
        
    def setup_directories(self):
        """Create input and output directories if they don't exist."""
        try:
            self.input_dir.mkdir(exist_ok=True)
            self.output_dir.mkdir(exist_ok=True)
            logger.info(f"Directories setup complete: {self.input_dir}, {self.output_dir}")
        except PermissionError:
            logger.error("Permission denied while creating directories")
            raise
        
    def get_pdf_files(self):
        """Get list of PDF files from input directory."""
        if not self.input_dir.exists():
            logger.error(f"Input directory {self.input_dir} does not exist")
            return []
        
        return list(self.input_dir.glob('*.pdf'))
    
    def convert_pdf(self, pdf_path):
        """Convert a single PDF file to images."""
        try:
            logger.info(f"Processing {pdf_path.name}")
            
            # Convert PDF to images
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                fmt=self.fmt.lower(),
                thread_count=os.cpu_count(),  # Optimize for multi-core systems
                grayscale=True,  # Better for OCR
                size=(None, None)  # Maintain original size
            )
            
            # Save images with progress bar
            for i, image in enumerate(tqdm(images, desc="Converting pages")):
                output_path = self.output_dir / f"page_{str(i + 1).zfill(3)}.{self.fmt.lower()}"
                image.save(
                    output_path,
                    format=self.fmt,
                    optimize=True,
                    quality=95  # High quality
                )
            
            logger.info(f"Successfully converted {len(images)} pages from {pdf_path.name}")
            return len(images)
            
        except PDFPageCountError:
            logger.error(f"Error: Invalid or corrupt PDF file: {pdf_path}")
            return 0
        except PDFSyntaxError:
            logger.error(f"Error: PDF syntax error in file: {pdf_path}")
            return 0
        except Exception as e:
            logger.error(f"Unexpected error processing {pdf_path}: {str(e)}")
            return 0

    def process_all_pdfs(self):
        """Process all PDF files in the input directory."""
        try:
            self.setup_directories()
            pdf_files = self.get_pdf_files()
            
            if not pdf_files:
                logger.warning("No PDF files found in input directory")
                return
            
            total_pages = 0
            for pdf_file in pdf_files:
                pages = self.convert_pdf(pdf_file)
                total_pages += pages
            
            logger.info(f"Conversion complete. Total pages processed: {total_pages}")
            
        except Exception as e:
            logger.error(f"Error during processing: {str(e)}")
            raise

def main():
    try:
        converter = PDFConverter()
        converter.process_all_pdfs()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()