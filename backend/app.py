from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.upload import router as upload_router
from backend.services.retrieval_service import RetrievalService
from backend.services.llm_service import LLMService
from backend.services.query_rewriter import rewrite_query
from backend.services.db_service import DBService

db = DBService()

app = FastAPI(title="Offline RAG Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)

# Load services once at startup — NOT inside RetrievalService
retriever = RetrievalService()
llm = LLMService()

class QuestionRequest(BaseModel):
    question: str
    session_id: str | None = None

@app.post("/ask")
def ask_question(data: QuestionRequest):

    if not data.session_id:
        session_id = db.create_session()
    else:
        session_id = data.session_id

    # Clean the query before retrieval (rule-based, instant — no LLM call)
    # Synonym expansion happens inside retriever.retrieve()
    cleaned_question = rewrite_query(data.question)

    # Retrieve using cleaned query; LLM gets original question for natural phrasing
    chunks = retriever.retrieve(cleaned_question)
    answer = llm.generate_answer(data.question, chunks)

    db.save_message(session_id, data.question, answer)

    return {
        "session_id": session_id,
        "question": data.question,
        "answer": answer
    }

@app.get("/sessions")
def get_sessions():
    # Uses the improved get_sessions_with_titles() from db_service
    sessions = db.get_sessions_with_titles()
    return sessions  # already returns [{"id": ..., "title": ...}]

@app.get("/chat/{session_id}")
def get_chat(session_id: str):
    msgs = db.get_messages(session_id)
    return [
        {"question": m["question"], "answer": m["answer"]}
        for m in msgs
    ]

@app.delete("/chat/{session_id}")
def delete_chat(session_id: str):
    db.delete_session(session_id)
    return {"message": "Chat deleted"}

@app.get("/")
def home():
    return {"status": "Backend running successfully"}