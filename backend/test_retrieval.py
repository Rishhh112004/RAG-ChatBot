from services.retrieval_service import RetrievalService

retriever = RetrievalService()

question = "Who is the manager?"

results = retriever.retrieve(question)

print("\nQUESTION:", question)

for r in results:
    print("\n--- RETRIEVED CHUNK ---")
    print("Upload ID:", r["upload_id"])
    print("Timestamp:", r["timestamp"])
    print("Text:", r["chunk_text"])