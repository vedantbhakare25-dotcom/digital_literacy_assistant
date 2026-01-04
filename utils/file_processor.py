import PyPDF2
import docx
from PIL import Image
import pytesseract
import io

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

def extract_text_from_docx(file):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error reading DOCX: {str(e)}")

def extract_text_from_image(file):
    """Extract text from image using OCR"""
    try:
        image = Image.open(file)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        raise Exception(f"Error reading image: {str(e)}")

def process_uploaded_file(uploaded_file):
    """
    Process uploaded file and extract text based on file type
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        str: Extracted text from the file
    """
    file_type = uploaded_file.type
    file_name = uploaded_file.name.lower()
    
    try:
        # PDF files
        if file_type == "application/pdf" or file_name.endswith('.pdf'):
            return extract_text_from_pdf(uploaded_file)
        
        # Word documents
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or file_name.endswith('.docx'):
            return extract_text_from_docx(uploaded_file)
        
        # Images
        elif file_type in ["image/png", "image/jpeg", "image/jpg"] or file_name.endswith(('.png', '.jpg', '.jpeg')):
            return extract_text_from_image(uploaded_file)
        
        # Plain text
        elif file_type == "text/plain" or file_name.endswith('.txt'):
            return uploaded_file.read().decode('utf-8')
        
        else:
            raise Exception(f"Unsupported file type: {file_type}")
    
    except Exception as e:
        raise Exception(f"Error processing file: {str(e)}")


