from services.text_processing import process_uploads
chunks = process_uploads()
for c in chunks:
    print("\n--- CHUNK ---")
    print("Upload ID:", c["upload_id"])
    print("Timestamp:", c["timestamp"])
    print("Text:", c["chunk_text"])