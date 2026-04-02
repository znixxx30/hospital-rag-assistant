from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import os

from app.ingest import load_split_embed_store
from app.rag import generate_answer

app = FastAPI()

# Temporary chat history (we'll improve later)
chat_history = []


class QueryRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "Hospital RAG Assistant Running"}


#  UPLOAD API
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_path = f"data/{file.filename}"

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process file (ingestion)
    load_split_embed_store(file_path)

    return {"message": "Document uploaded and processed successfully"}


@app.post("/query")
def query(req: QueryRequest):
    answer, chunks = generate_answer(req.question)

    # Extract page sources
    sources = [f"page {c['metadata']['page']}" for c in chunks]

    return {
        "answer": answer,
        "sources": list(set(sources))
    }