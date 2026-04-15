import pdfplumber
from pypdf import PdfReader
import docx


def load_file(file_path):

    if file_path.endswith(".pdf"):

        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() + "\n"

        return text

    elif file_path.endswith(".docx"):

        doc = docx.Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])

        return text

    elif file_path.endswith(".txt"):

        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    else:
        print("Unsupported file type")
        return ""