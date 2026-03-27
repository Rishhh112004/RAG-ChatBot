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

    file_path = "data/knowledge_store.txt"

    import re
    import numpy as np
    from datetime import datetime
    from services.embedding_service import EmbeddingService

    # Read existing data
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            existing_data = f.read()
    except:
        existing_data = ""

    # Split new paragraph into sentences
    new_sentences = re.split(r'(?<=[.!?])\s+', paragraph)
    new_sentences = [s.strip() for s in new_sentences if s.strip()]

    # Extract existing sentences
    existing_sentences = set()

    blocks = existing_data.split("---UPLOAD START---")

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        text = block.split("\n", 1)[1].replace("---UPLOAD END---", "").strip()

        sentences = re.split(r'(?<=[.!?])\s+', text)

        for s in sentences:
            s = s.strip()
            if s:
                existing_sentences.add(s)

    # 🔥 Semantic Deduplication
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

    # If nothing new
    if len(unique_sentences) == 0:
        print("\nDuplicate information detected. Nothing new added.\n")
        return

    # Save only new sentences
    final_text = " ".join(unique_sentences)

    with open(file_path, "a", encoding="utf-8") as f:
        f.write("\n---UPLOAD START---\n")
        f.write(f"Timestamp: {datetime.now()}\n")
        f.write(final_text + "\n")
        f.write("---UPLOAD END---\n")

    print("\nOnly new information stored.\n")

    rebuild_index()
    
# NEW FUCTION TO DELETE PARAGRAPH 
def delete_paragraph():

    import re

    file_path = "data/knowledge_store.txt"

    # Read file
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract blocks correctly
    blocks = re.findall(r"---UPLOAD START---(.*?)---UPLOAD END---", content, re.DOTALL)

    uploads = [block.strip() for block in blocks if block.strip()]

    if len(uploads) == 0:
        print("\nNo paragraphs available.\n")
        return

    # 🔥 Print ALL paragraphs first
    print("\nUploaded Paragraphs:\n")

    for i, block in enumerate(uploads):

        lines = block.split("\n", 1)

        if len(lines) > 1:
            text = lines[1].strip()
        else:
            text = block.strip()

        preview = text[:80].replace("\n", " ")

        print(f"{i+1}. {preview}...")

    # 🔥 THEN take input (OUTSIDE loop)
    try:
        choices = input("\nEnter paragraph numbers to delete (comma separated): ")

        indices = list(set(int(x.strip()) for x in choices.split(",")))

        # Validate indices
        for idx in indices:
            if idx < 1 or idx > len(uploads):
                print("\nInvalid selection\n")
                return

    except:
        print("\nInvalid input\n")
        return

    # Delete in reverse order
    for idx in sorted(indices, reverse=True):
        del uploads[idx - 1]

    # Rebuild file
    new_content = ""

    for block in uploads:
        new_content += "\n---UPLOAD START---\n"
        new_content += block.strip() + "\n"
        new_content += "---UPLOAD END---\n"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("\nParagraph(s) deleted successfully.\n")

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
    