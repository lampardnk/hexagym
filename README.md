# LaTeX to PDF Web Converter

A simple web application that converts LaTeX code to PDF using Python Flask.

## Prerequisites

- Python 3.x
- pdflatex (TeXLive or MiKTeX)
- pip (Python package manager)

## Installation

1. Clone this repository or download the files
2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```
3. Ensure pdflatex is installed and available in your system PATH

## Usage

1. Start the application:
   ```
   python app.py
   ```
2. Open your web browser and navigate to `http://localhost:5000`
3. Enter your LaTeX code in the input box
4. Click "Compile to PDF" to generate and view the PDF

## Features

- Real-time PDF preview
- Error handling and status messages
- Automatic logging of operations in `log.json`
- Clean and modern user interface

## File Structure

- `app.py` - Flask backend application
- `static/index.html` - Frontend interface
- `requirements.txt` - Python dependencies
- `tex_files/` - Directory for temporary LaTeX files
- `pdf_files/` - Directory for generated PDFs
- `log.json` - Operation logs

## Log Format

The `log.json` file contains entries with the following information:
- Timestamp of the operation
- Input tex file path
- Output PDF file path
- Success status
- Error code (if any) 