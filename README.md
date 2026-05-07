# Offline RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built to run locally without external API calls. It uses local document uploads, semantic search, and a local LLM model to answer questions based on your uploaded content.

## What is RAG?

Retrieval-Augmented Generation (RAG) improves language model answers by retrieving relevant knowledge from uploaded documents before generating a response. This reduces hallucinations and keeps answers grounded in your content.

## Features

- **Offline-first design**: No internet access required for inference
- **Semantic search**: Embeddings + FAISS vector search
- **Multiple upload formats**: PDF, DOCX, TXT, and paragraph text
- **Duplicate detection**: Filters redundant text during upload
- **Web interface**: Browser-based chat UI with session history
- **Local MongoDB storage**: Persists uploaded content and conversations
- **Local LLM support**: Uses `llama-cpp-python` with a GGUF Mistral model

## Architecture

```
User input → Text extraction → Duplicate filtering → Chunking → Embedding → FAISS search → LLM generation → Answer
```

## Folder Structure

```
rag_chatbot/
├── backend/                    # FastAPI backend implementation
│   ├── routes/                 # API endpoints
│   ├── services/               # Business logic and helpers
│   ├── app.py                  # Main FastAPI app
│   └── build_vector_store.py   # Rebuilds local FAISS index from stored text
├── frontend/                   # Web chat UI
│   ├── index.html              # Main UI
│   ├── script.js               # Frontend behavior
│   └── style.css               # Styles
├── models/                     # Local GGUF model files
├── vector_store/               # Optional generated index files
├── nltk_data/                  # Optional NLTK data directory
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── SRS.md                      # Requirements specification
```

## Installation

### Prerequisites

- Python 3.11+
- MongoDB running locally on port `27017`
- Git

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Rishhh112004/RAG-ChatBot.git
   cd rag_chatbot
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download the Mistral GGUF model and put it in `models/` as `mistral.gguf`.
5. Start MongoDB locally.

## Running the App

### Start the backend server

```bash
uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

### Open the frontend

- Open `frontend/index.html` in your browser
- Or use a local server for better compatibility:
  ```bash
  python -m http.server 8080
  ```

### Use the chatbot

- Upload files using the upload control
- Paste paragraph text using the text input
- Ask questions in the chat box
- Answers are generated from uploaded content

## API Endpoints

- `POST /upload-file` — Upload PDF, DOCX, or TXT files
- `POST /upload-text` — Upload a text paragraph
- `POST /ask` — Ask a question and get an answer
- `GET /sessions` — List saved chat sessions
- `GET /chat/{session_id}` — Retrieve chat history
- `DELETE /chat/{session_id}` — Delete a saved chat session

### Example: Upload paragraph

```http
POST /upload-text
Content-Type: application/json

{
  "paragraph": "This is the text to add to the knowledge base."
}
```

### Example: Ask a question

```http
POST /ask
Content-Type: application/json

{
  "question": "What is MOIL?",
  "session_id": "optional_session_id"
}
```

## Rebuilding the Vector Store

If you need to rebuild the semantic index, run:

```bash
python backend/build_vector_store.py
```

## Notes

- The repository currently supports the browser-based UI.
- Uploaded text is stored in MongoDB and indexed with FAISS.
- Generated index files include `vector_store.index` and `chunks.pkl`.

## Troubleshooting

- **Model not found**: Verify `models/mistral.gguf` exists.
- **MongoDB error**: Start MongoDB and ensure it is reachable at `mongodb://localhost:27017/`.
- **Frontend issues**: Use a local HTTP server if the browser blocks file-based fetch requests.

## Dependencies

- Python 3.11+
- MongoDB 4.0+
- GGUF-compatible Mistral model (~4GB)

## Performance

- Embedding model: `sentence-transformers/all-MiniLM-L6-v2`
- Vector search: FAISS `IndexFlatL2`
- Chunking strategy is implemented in `backend/services/text_processing.py`
- Retrieval uses local semantic search and LLM generation

   - Upload documents using the file input
   - Ask questions in the chat interface
   - Responses are generated based on uploaded content

## API Documentation

### Endpoints

- `POST /upload` - Upload documents (PDF, DOCX, TXT) or text paragraphs
- `POST /ask` - Ask questions to the chatbot

#### Upload Endpoint
```json
POST /upload
Content-Type: multipart/form-data

{
  "file": "document.pdf"
}
```

#### Ask Endpoint
```json
POST /ask
Content-Type: application/json

{
  "question": "What is MOIL?",
  "session_id": "optional_session_id"
}
```

## Configuration

- MongoDB connection: localhost:27017
- Model path: `models/mistral.gguf`
- Vector store: `vector_store/faiss.index`

## Troubleshooting

- **Model not found**: Ensure Mistral GGUF model is downloaded and placed in `models/` directory
- **MongoDB connection error**: Start MongoDB service locally
- **Import errors**: Activate virtual environment and install dependencies
- **Vector store issues**: Rebuild vector store using `python backend/build_vector_store.py`

## Dependencies

- Python 3.11+
- MongoDB 4.0+
- GGUF-compatible Mistral model (~4GB)

## Performance

- Embedding model: sentence-transformers/all-MiniLM-L6-v2
- Vector search: FAISS IndexFlatL2
- Chunk size: Configurable in text_processing.py
- Top-k retrieval: 4 chunks

## Working Screenshots

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/1dd04ccb-0b37-471b-869b-18287f1de74f" />

<img width="1919" height="996" alt="image" src="https://github.com/user-attachments/assets/d371a800-f30a-4faf-a369-694cb6af8470" />

