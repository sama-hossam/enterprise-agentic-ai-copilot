from fastapi import APIRouter, HTTPException
from app.schemas.rag import AskRequest, AskResponse
from app.rag.retrieval import retrieve
from app.rag.generation import generate_answer

router = APIRouter(prefix="/api/v1/rag", tags=["rag"])

@router.post("/ask", response_model=AskResponse)
def ask_rag(payload: AskRequest):
    try:
        evidence = retrieve(payload.question, payload.department, payload.top_k)
        answer, mode = generate_answer(payload.question, evidence)
        return AskResponse(mode=mode, answer=answer, evidence=evidence)
    except ImportError as exc:
        raise HTTPException(status_code=503, detail="Install the RAG extra: uv sync --extra rag --extra dev") from exc
