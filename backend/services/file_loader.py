import pdfplumber
import docx
import docx.table
import docx.text.paragraph
from docx.oxml.ns import qn

def load_file(file_path: str) -> str:

    if file_path.endswith(".pdf"):
        return _load_pdf(file_path)

    elif file_path.endswith(".docx"):
        return _load_docx(file_path)

    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    else:
        print(f"Unsupported file type: {file_path}")
        return ""

def _load_pdf(file_path: str) -> str:

    full_text = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:

            # --- Extract tables first ---
            tables = page.extract_tables()
            table_cell_words = set()  # track table content to avoid duplication

            for table in tables:
                if not table:
                    continue
                table_lines = []
                for row in table:
                    if not row:
                        continue
                    # Clean None values, join with pipe separator
                    cleaned_cells = [str(cell).strip() if cell else "" for cell in row]
                    row_text = " | ".join(c for c in cleaned_cells if c)
                    if row_text.strip():
                        table_lines.append(row_text)
                        # Track all cell text to filter from plain text extraction
                        for cell in cleaned_cells:
                            for word in cell.lower().split():
                                table_cell_words.add(word)

                if table_lines:
                    full_text.append("\n".join(table_lines))

            # --- Extract plain page text ---
            page_text = page.extract_text()
            if page_text:
                full_text.append(page_text.strip())

    return "\n\n".join(part for part in full_text if part.strip())

def _load_docx(file_path: str) -> str:

    doc = docx.Document(file_path)
    full_text = []

    for child in doc.element.body:

        # --- Paragraph ---
        if child.tag == qn('w:p'):
            para = docx.text.paragraph.Paragraph(child, doc)
            text = para.text.strip()
            if text:
                full_text.append(text)

        # --- Table ---
        elif child.tag == qn('w:tbl'):
            table = docx.table.Table(child, doc)
            table_lines = []

            for row in table.rows:
                cells = [cell.text.strip() for cell in row.cells]

                # Deduplicate adjacent cells (merged cells repeat in python-docx)
                deduped = []
                prev = None
                for cell in cells:
                    if cell != prev:
                        deduped.append(cell)
                    prev = cell

                row_text = " | ".join(c for c in deduped if c)
                if row_text:
                    table_lines.append(row_text)

            if table_lines:
                full_text.append("\n".join(table_lines))

    return "\n\n".join(part for part in full_text if part.strip())