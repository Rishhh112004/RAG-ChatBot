from services.retrieval_service import RetrievalService
from services.llm_service import LLMService
from services.text_processing import process_uploads
from services.embedding_service import EmbeddingService
from services.vector_store import VectorStore


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

    with open("data/knowledge_store.txt", "a", encoding="utf-8") as f:

        from datetime import datetime

        f.write("\n---UPLOAD START---\n")
        f.write(f"Timestamp: {datetime.now()}\n")
        f.write(paragraph + "\n")
        f.write("---UPLOAD END---\n")

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
        print("3. Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":
            ask_question()

        elif choice == "2":
            upload_paragraph()

        elif choice == "3":
            print("\nExiting...\n")
            break

        else:
            print("\nInvalid choice")


if __name__ == "__main__":
    main()
    