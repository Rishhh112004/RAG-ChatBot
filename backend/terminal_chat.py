from services.retrieval_service import RetrievalService
from services.llm_service import LLMService
from services.text_processing import process_uploads
from services.embedding_service import EmbeddingService
from services.vector_store import VectorStore
import numpy as np


def rebuild_index():

    chunks = process_uploads()

    texts = [c["chunk_text"] for c in chunks]

    embedder = EmbeddingService()

    embeddings = embedder.embed_texts(texts)

    store = VectorStore()

    store.add_vectors(embeddings, chunks)

    store.save()

    print("\nVector database updated.\n")


def upload_paragraph():
    paragraph = input("\nPaste paragraph:\n")
    import re
    import numpy as np
    from services.embedding_service import EmbeddingService
    from services.db_service import DBService
    db = DBService()
    # Get existing data from MongoDB
    existing_data = db.get_all_paragraphs()
    existing_sentences = set()
    for item in existing_data:
        text = item["text"]
        sentences = re.split(r'(?<=[.!?])\s+', text)
        for s in sentences:
            s = s.strip()
            if s:
                existing_sentences.add(s)
    # Split new paragraph
    new_sentences = re.split(r'(?<=[.!?])\s+', paragraph)
    new_sentences = [s.strip() for s in new_sentences if s.strip()]
    # Semantic dedup
    embedder = EmbeddingService()
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
        print("\nDuplicate information detected. Nothing new added.\n")
        return
    final_text = " ".join(unique_sentences)
    # Store in MongoDB (instead of .txt file)
    db.insert_paragraph(final_text)
    print("\nOnly new information stored in database.\n")
    rebuild_index()


# NEW FUNCTION TO DELETE PARAGRAPH
def delete_paragraph():
    from services.db_service import DBService
    db = DBService()
    data = db.get_all_paragraphs()
    if len(data) == 0:
        print("\nNo paragraphs available.\n")
        return
    print("\nUploaded Paragraphs:\n")
    for i, item in enumerate(data):
        text = item["text"]
        preview = text[:80].replace("\n", " ")
        print(f"{i+1}. {preview}...")
    try:
        choices = input("\nEnter paragraph numbers to delete (comma separated): ")
        indices = list(set(int(x.strip()) for x in choices.split(",")))
        for idx in indices:
            if idx < 1 or idx > len(data):
                print("\nInvalid selection\n")
                return
    except:
        print("\nInvalid input\n")
        return
    # Get MongoDB IDs
    ids_to_delete = [str(data[i-1]["_id"]) for i in indices]
    db.delete_paragraphs(ids_to_delete)
    print("\nParagraph(s) deleted successfully from database.\n")
    rebuild_index()


def ask_question():

    question = input("\nAsk question:\n")

    retriever = RetrievalService()
    llm = LLMService()

    chunks = retriever.retrieve(question)

    answer = llm.generate_answer(question, chunks)

    print("\nANSWER:\n")
    print(answer)
    print("\n")


def main():

    print("\nOffline RAG Chatbot (Terminal Mode)")
    print("------------------------------------")

    while True:

        print("\nChoose option:")
        print("1. Ask Question")
        print("2. Upload Paragraph")
        print("3. Delete Paragraph")
        print("4. Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":
            ask_question()

        elif choice == "2":
            upload_paragraph()

        elif choice == "3":
            delete_paragraph()

        elif choice == "4":
            print("\nExiting...\n")
            break

        else:
            print("\nInvalid choice")


if __name__ == "__main__":
    main()
    