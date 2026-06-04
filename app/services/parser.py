import pdfplumber
import os

def extract_text_from_pdf(file_path):
    """Extracts text from a given PDF file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No such file: {file_path}")
        
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return None
        
    return text.strip()
