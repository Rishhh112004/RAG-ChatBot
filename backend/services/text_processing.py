# WITH THE CODE BELOW, THE DATA IS GETTING STORED IN MONGODB DATABASE

from services.db_service import DBService
def process_uploads():
    db = DBService()
    data = db.get_all_paragraphs()
    chunks = []
    import re
    for item in data:
        text = item["text"]
        upload_id = str(item["_id"])
        timestamp = item["timestamp"]
        sentences = re.split(r'(?<=[.!?])\s+', text)
        for i in range(len(sentences) - 1):
            chunk_text = sentences[i] + " " + sentences[i+1]
            chunks.append({
                "upload_id": upload_id,
                "timestamp": timestamp,
                "chunk_text": chunk_text
            })
    return chunks
