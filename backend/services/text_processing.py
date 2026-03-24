import re
import os
from typing import List, Dict



UPLOAD_FILE = "data/knowledge_store.txt"


def read_uploads() -> List[Dict]:

    with open(UPLOAD_FILE, "r", encoding="utf-8") as file:
        content = file.read()

    uploads = []
    blocks = content.split("---UPLOAD START---")

    upload_id = 0

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        upload_id += 1

        timestamp_match = re.search(r"Timestamp:(.*)", block)
        timestamp = timestamp_match.group(1).strip() if timestamp_match else "unknown"

        text = block.split("\n", 1)[1].replace("---UPLOAD END---", "").strip()

        uploads.append({
            "upload_id": upload_id,
            "timestamp": timestamp,
            "text": text
        })

    return uploads


def split_into_sentences(text: str):

    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def create_chunks(
    sentences: List[str],
    chunk_size: int = 3,
    overlap: int = 1
) -> List[str]:
    """
    Creates overlapping chunks from sentences.
    """
    chunks = []
    start = 0

    while start < len(sentences):
        end = start + chunk_size
        chunk = sentences[start:end]
        chunks.append(" ".join(chunk))
        start = end - overlap

    return chunks


def process_uploads() -> List[Dict]:

    processed_chunks = []
    uploads = read_uploads()

    for upload in uploads:
        sentences = split_into_sentences(upload["text"])
        chunks = create_chunks(sentences)

        for chunk in chunks:
            processed_chunks.append({
                "upload_id": upload["upload_id"],
                "timestamp": upload["timestamp"],
                "chunk_text": chunk
            })

    return processed_chunks