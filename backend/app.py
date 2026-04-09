from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.upload import router as upload_router
from backend.services.retrieval_service import RetrievalService
from backend.services.llm_service import LLMService


app = FastAPI(title="Offline RAG Chatbot")

# CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include upload routes
app.include_router(upload_router)

# Initialize services
retriever = RetrievalService()
llm = LLMService()


# Request schema
class QuestionRequest(BaseModel):
    question: str


# 🔥 ADD THIS (IMPORTANT)
@app.post("/ask")
def ask_question(data: QuestionRequest):

    chunks = retriever.retrieve(data.question)

    answer = llm.generate_answer(data.question, chunks)

    return {
        "answer": answer
    }


# Root check
@app.get("/")
def home():
    return {"status": "Backend running successfully"}