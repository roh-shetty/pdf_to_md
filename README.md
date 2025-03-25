# PDF to Markdown Converter

## Overview

This Python script takes a scanned PDF file and transforms it into a structured markdown document through a multi-step process:
1. Converts each page of the PDF to an image using `pdf2image`
2. Processes each image with Tesseract OCR to extract text
3. Extracts the text using OCR, and converts it to a formatted markdown document, preserving some of the original structure like headings and lists.

## Prerequisites

Before you begin, ensure you have the following installed:

### System Dependencies
- Python 3.7+
- Tesseract OCR
- Poppler (for PDF conversion)

### Installation Instructions

#### For Ubuntu/Debian
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y tesseract-ocr poppler-utils python3-pip

# Install Python packages
pip3 install pytesseract pdf2image
```

#### For macOS (using Homebrew)
```bash
# Install system dependencies
brew install tesseract poppler

# Install Python packages
pip install pytesseract pdf2image
```

#### For Windows
1. Download and install Tesseract OCR from the official GitHub repository
2. Add Tesseract to your system PATH
3. Install Poppler for Windows
4. Use pip to install Python packages

### Python Package Requirements
Install the required Python packages:
```bash
pip install pytesseract pdf2image
```

## Usage

### Basic Usage
```bash
python pdf_to_markdown.py input.pdf
```

### Advanced Usage
```bash
# Specify output file
python pdf_to_markdown.py input.pdf -o output.md

# Adjust DPI for better quality (default is 300)
python pdf_to_markdown.py input.pdf --dpi 400
```

## Parameters
- `pdf_path`: Path to the input PDF file (required)
- `--output` or `-o`: Path for the output markdown file (optional)
- `--dpi`: DPI for PDF conversion (default: 300)

## Features
- Converts scanned PDFs to markdown
- Preserves document structure
- Supports custom DPI settings


## Dependencies
- `pytesseract`: OCR text extraction
- `pdf2image`: PDF to image conversion

