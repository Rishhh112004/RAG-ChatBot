# from fastapi import FastAPI
# from routes.upload import upload_router

# app = FastAPI(title="Offline RAG Chatbot")

# app.include_router(upload_router)

# @app.get("/")
# def home():
#     return {"status": "Backend running successfully"}

# RUNS SUCCESSFULLY WITHOUT FRONTEND
from fastapi import FastAPI
from backend.routes.upload import router as upload_router

app = FastAPI(title="Offline RAG Chatbot")

app.include_router(upload_router)

@app.get("/")
def home():
    return {"status": "Backend running successfully"}



# from fastapi import FastAPI
# from backend.routes.upload import router as upload_router

# # NEW IMPORTS
# from pydantic import BaseModel
# from backend.services.retrieval_service import RetrievalService
# from backend.services.llm_service import LLMService

# app = FastAPI(title="Offline RAG Chatbot")

# app.include_router(upload_router)


# @app.get("/")
# def home():
#     return {"status": "Backend running successfully"}


# # -----------------------------
# # RAG Question Answering System
# # -----------------------------

# retriever = RetrievalService()
# llm = LLMService()


# class QuestionRequest(BaseModel):
#     question: str


# @app.post("/ask")
# def ask_question(data: QuestionRequest):

#     chunks = retriever.retrieve(data.question)

#     answer = llm.generate_answer(data.question, chunks)

#     return {
#         "question": data.question,
#         "answer": answer
#     }