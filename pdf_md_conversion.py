import argparse
import os
from pathlib import Path
import pytesseract
from pdf2image import convert_from_path
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_path, dpi=300):
    """
    Extract text from a scanned PDF using OCR.
    
    Args:
        pdf_path (str): Path to the PDF file
        dpi (int): DPI for the conversion (higher means better quality but slower)
    
    Returns:
        list: List of strings, each representing text from one page
    """
    logger.info(f"Converting PDF to images: {pdf_path}")
    try:
        # Convert PDF to images
        images = convert_from_path(pdf_path, dpi=dpi)
        
        # Extract text from each image using OCR
        pages_text = []
        for i, img in enumerate(images):
            logger.info(f"Performing OCR on page {i+1}/{len(images)}")
            text = pytesseract.image_to_string(img)
            pages_text.append(text)
            
        return pages_text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        raise

def text_to_markdown(pages_text):
    """
    Convert extracted text to markdown format.
    
    Args:
        pages_text (list): List of strings, each representing text from one page
    
    Returns:
        str: Markdown formatted text
    """
    markdown_text = ""
    
    for page_num, text in enumerate(pages_text):
        # Add page number as header
        markdown_text += f"## Page {page_num + 1}\n\n"
        
        # Process text line by line
        lines = text.split('\n')
        paragraph = ""
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                if paragraph:
                    markdown_text += paragraph + "\n\n"
                    paragraph = ""
                continue
            
            # Check if line might be a header (all caps or ending with colon)
            if line.isupper() or line.endswith(':'):
                if paragraph:
                    markdown_text += paragraph + "\n\n"
                    paragraph = ""
                markdown_text += f"### {line}\n\n"
            
            # Check if line might be a list item
            elif line.startswith(('- ', '• ', '* ', '1. ', '2. ')):
                if paragraph:
                    markdown_text += paragraph + "\n\n"
                    paragraph = ""
                markdown_text += f"{line}\n"
            
            # Otherwise, treat as paragraph text
            else:
                if paragraph:
                    paragraph += " " + line
                else:
                    paragraph = line
        
        # Add any remaining paragraph
        if paragraph:
            markdown_text += paragraph + "\n\n"
    
    return markdown_text

def save_markdown(markdown_text, output_path):
    """
    Save markdown text to a file.
    
    Args:
        markdown_text (str): Markdown text to save
        output_path (str): Path to save the markdown file
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
        logger.info(f"Markdown file saved to: {output_path}")
    except Exception as e:
        logger.error(f"Error saving markdown file: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Convert scanned PDF to markdown.')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('--output', '-o', help='Output markdown file path')
    parser.add_argument('--dpi', type=int, default=300, help='DPI for PDF conversion (default: 300)')
    
    args = parser.parse_args()
    
    # If output path is not specified, use the PDF filename with .md extension
    if not args.output:
        output_path = Path(args.pdf_path).with_suffix('.md')
    else:
        output_path = args.output
    
    logger.info("Starting PDF to markdown conversion")
    
    try:
        # Extract text using OCR
        pages_text = extract_text_from_pdf(args.pdf_path, args.dpi)
        
        # Convert text to markdown
        markdown_text = text_to_markdown(pages_text)
        
        # Save to markdown file
        save_markdown(markdown_text, output_path)
        
        logger.info("Conversion complete!")
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())