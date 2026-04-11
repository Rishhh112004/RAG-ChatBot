# Offline RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that operates entirely offline, combining semantic search with large language models for accurate, context-aware responses based on uploaded documents.

## What is RAG?

Retrieval-Augmented Generation (RAG) is an AI technique that enhances language model responses by retrieving relevant information from a knowledge base before generating answers. This approach improves accuracy and reduces hallucinations compared to standalone generative models.

## Features

- **Offline Operation**: No external API calls required - runs entirely on local hardware
- **Semantic Search**: Uses embeddings and FAISS vector database for intelligent document retrieval
- **Multiple File Formats**: Supports PDF, DOCX, and TXT file uploads or user can directly upload paragraph 
- **Duplicate Detection**: Automatically removes redundant information during uploads
- **Web Interface**: Clean HTML/CSS/JavaScript frontend for easy interaction
- **Terminal Interface**: Alternative command-line interface for advanced users
- **MongoDB Storage**: Persistent document storage with metadata
- **Mistral LLM Integration**: Powered by local GGUF models for inference

## Architecture

```
Query → Embedding → Vector Search → Context Retrieval → LLM Generation → Response

1. User uploads documents (PDF/DOCX/TXT) or paragraphs itself diectly
2. Text is extracted and stored in MongoDB
3. Documents are chunked and embedded using Sentence Transformers
4. Embeddings are indexed in FAISS vector database
5. User asks a question
6. Question is embedded and searched against the vector database
7. Top-k relevant chunks are retrieved as context
8. Context is fed to Mistral LLM for answer generation
9. Response is returned to user
```

## Folder Structure

```
rag_chatbot/
├── backend/                    # Python FastAPI backend
│   ├── routes/                 # API endpoints
│   │   ├── query.py           # Question answering endpoint
│   │   └── upload.py          # File upload endpoint
│   ├── services/              # Core business logic
│   │   ├── db_service.py      # MongoDB operations
│   │   ├── embedding_service.py # Text embeddings
│   │   ├── file_loader.py     # Document parsing
│   │   ├── llm_service.py     # Mistral model inference
│   │   ├── retrieval_service.py # Vector search
│   │   ├── text_processing.py # Text chunking
│   │   └── vector_store.py    # FAISS operations
│   ├── app.py                 # FastAPI application
│   ├── terminal_chat.py       # CLI interface
│   └── config.py              # Configuration (empty)
├── frontend/                   # Web interface
│   ├── index.html             # Main HTML page
│   ├── script.js              # Frontend JavaScript
│   └── style.css              # CSS styling
├── data/                      # Sample knowledge base
│   └── knowledge_store.txt    # Text data storage
├── models/                    # LLM model files (GGUF)
├── vector_store/              # FAISS index and metadata
├── nltk_data/                 # NLTK data (if used)
├── requirements.txt           # Python dependencies
├── run_chatbot.ps1           # PowerShell launcher
└── README.md                 # This file
```

## Installation

### Prerequisites

- Python 3.11+
- MongoDB (running locally on default port 27017)
- Git

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Rishhh112004/RAG-ChatBot.git
   cd rag_chatbot
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Download Mistral GGUF model:**
   - Download `mistral-7b-instruct-v0.1.Q4_K_M.gguf` (or similar) from Hugging Face
   - Place it in the `models/` directory as `mistral.gguf`
   - Note: Model files are large (~4GB) and not included in this repository

6. **Start MongoDB:**
   Ensure MongoDB is running locally on port 27017

## Usage

### Web Interface (Recommended)

1. **Start the backend server:**
   ```bash
   uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Open the frontend:**
   - Open `frontend/index.html` in your web browser
   - Or serve it via a local HTTP server for better functionality

3. **Use the chatbot:**
   - Upload documents using the file input
   - Ask questions in the chat interface
   - Responses are generated based on uploaded content

### Terminal Interface

Run the PowerShell script:
```powershell
.\run_chatbot.ps1
```

This provides a command-line interface for uploading files, asking questions, and managing documents.

## Testing

Run the test files to verify functionality:

```bash
# Test RAG pipeline
python backend/test_rag_pipeline.py

# Test retrieval
python backend/test_retrieval.py

# Test text processing
python backend/test_text_processing.py
```

## Future Improvements

- Support for additional file formats (images, audio)
- Integration with other LLM models (Llama, GPT-J)
- Web-based document management interface
- Conversation history and context
- Multi-language support
- Performance optimizations for large document sets
- Docker containerization
- REST API documentation with Swagger/OpenAPI

## License

This project is open source. Please check individual component licenses for compliance.

## Contributing

Contributions are welcome! Please create issues for bugs or feature requests, and submit pull requests for improvements.