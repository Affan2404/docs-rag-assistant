from fastapi import FastAPI
from pydantic import BaseModel
from generate import answer_question

app = FastAPI(title="Freshdesk Docs RAG Assistant")

class QueryRequest(BaseModel):
    question: str

class SourceChunk(BaseModel):
    source_file: str
    distance: float

class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    answer, chunks = answer_question(request.question)

    sources = [
        SourceChunk(source_file=c["source_file"], distance=c["distance"])
        for c in chunks
    ]

    return QueryResponse(answer=answer, sources=sources)