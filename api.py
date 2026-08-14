from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from generate import answer_question
from logger import logger

app = FastAPI(title="Freshdesk Docs RAG Assistant")

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, description="The question to ask")

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
    try:
        answer, chunks = answer_question(request.question)
    except Exception as e:
        logger.error(f"Unexpected error handling query='{request.question}': {e}")
        raise HTTPException(
            status_code=500,
            detail="Something went wrong processing your question. Please try again."
        )

    sources = [
        SourceChunk(source_file=c["source_file"], distance=c["distance"])
        for c in chunks
    ]

    return QueryResponse(answer=answer, sources=sources)