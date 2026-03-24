from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

UPLOAD_FILE = "data/knowledge_store.txt"

router = APIRouter(prefix="/upload", tags=["Upload"])

class UploadRequest(BaseModel):
    paragraph: str


@router.post("/")
def upload_paragraph(data: UploadRequest):
    with open(UPLOAD_FILE, "a", encoding="utf-8") as file:
        file.write("\n---UPLOAD START---\n")
        file.write(f"Timestamp: {datetime.now()}\n")
        file.write(data.paragraph.strip() + "\n")
        file.write("---UPLOAD END---\n")

    return {"message": "Paragraph uploaded successfully"}
