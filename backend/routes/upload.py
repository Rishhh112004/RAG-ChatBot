from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from datetime import datetime
import re
import numpy as np

from backend.services.db_service import DBService
from backend.services.embedding_service import EmbeddingService
from backend.services.file_loader import load_file

router = APIRouter(tags=["Upload"])

db = DBService()
embedder = EmbeddingService()


# =========================
#  TEXT PARAGRAPH UPLOAD
# =========================

class UploadRequest(BaseModel):
    paragraph: str


@router.post("/upload-text")
def upload_paragraph(data: UploadRequest):

    paragraph = data.paragraph.strip()

    if not paragraph:
        return {"message": "Empty paragraph"}

    #  Fetch existing data
    existing_data = db.get_all_paragraphs()

    existing_sentences = set()

    for item in existing_data:
        sentences = re.split(r'(?<=[.!?])\s+', item["text"])
        for s in sentences:
            s = s.strip()
            if s:
                existing_sentences.add(s)

    #  New sentences
    new_sentences = re.split(r'(?<=[.!?])\s+', paragraph)
    new_sentences = [s.strip() for s in new_sentences if s.strip()]

    existing_list = list(existing_sentences)

    unique_sentences = []

    for new_s in new_sentences:

        is_duplicate = False

        if existing_list:
            new_vec = embedder.embed_query(new_s)
            existing_vecs = embedder.embed_texts(existing_list)

            similarities = np.dot(existing_vecs, new_vec) / (
                np.linalg.norm(existing_vecs, axis=1) * np.linalg.norm(new_vec)
            )

            if max(similarities) > 0.85:
                is_duplicate = True

        if not is_duplicate:
            unique_sentences.append(new_s)

    if len(unique_sentences) == 0:
        return {"message": "Duplicate information. Nothing added."}

    final_text = " ".join(unique_sentences)

    db.insert_paragraph(final_text)

    return {"message": "New information stored successfully"}


# =========================
#  FILE UPLOAD (PDF/DOCX/TXT)
# =========================

@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):

    try:
        # Save temporarily
        temp_path = f"temp_{file.filename}"

        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # Extract text
        text = load_file(temp_path)

        if not text.strip():
            return {"message": "No text extracted from file"}

        #  Fetch existing data
        existing_data = db.get_all_paragraphs()

        existing_sentences = set()

        for item in existing_data:
            sentences = re.split(r'(?<=[.!?])\s+', item["text"])
            for s in sentences:
                s = s.strip()
                if s:
                    existing_sentences.add(s)

        #  New sentences
        new_sentences = re.split(r'(?<=[.!?])\s+', text)
        new_sentences = [s.strip() for s in new_sentences if s.strip()]

        existing_list = list(existing_sentences)

        unique_sentences = []

        for new_s in new_sentences:

            is_duplicate = False

            if existing_list:
                new_vec = embedder.embed_query(new_s)
                existing_vecs = embedder.embed_texts(existing_list)

                similarities = np.dot(existing_vecs, new_vec) / (
                    np.linalg.norm(existing_vecs, axis=1) * np.linalg.norm(new_vec)
                )

                if max(similarities) > 0.85:
                    is_duplicate = True

            if not is_duplicate:
                unique_sentences.append(new_s)

        if len(unique_sentences) == 0:
            return {"message": "Duplicate file content. Nothing added."}

        final_text = " ".join(unique_sentences)

        db.insert_paragraph(final_text)

        return {"message": f"{file.filename} processed and stored"}

    except Exception as e:
        return {"message": f"Error: {str(e)}"}