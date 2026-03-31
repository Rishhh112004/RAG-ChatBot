# RUNS SUCCESSFULLY WITHOUT FRONTEND
from fastapi import FastAPI
from backend.routes.upload import router as upload_router

app = FastAPI(title="Offline RAG Chatbot")

app.include_router(upload_router)

@app.get("/")
def home():
    return {"status": "Backend running successfully"}