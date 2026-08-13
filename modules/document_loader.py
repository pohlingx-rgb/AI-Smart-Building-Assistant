from pypdf import PdfReader
from docx import Document

def read_pdf(uploaded_file):
    """
    Read text from a PDF file uploaded via Streamlit.
    """
    text = ""
    pdf = PdfReader(uploaded_file)
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()

def read_docx(uploaded_file):
    """
    Read text from a DOCX file uploaded via Streamlit.
    """
    text = ""
    doc = Document(uploaded_file)
    for para in doc.paragraphs:
        if para.text.strip():
            text += para.text + "\n"
    return text.strip()

def read_txt(uploaded_file):
    """
    Read text from a TXT file uploaded via Streamlit.
    """
    return uploaded_file.read().decode("utf-8").strip()
