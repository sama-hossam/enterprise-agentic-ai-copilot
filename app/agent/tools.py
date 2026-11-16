from typing import Literal

from pydantic import BaseModel, Field

from app.rag.retrieval import retrieve


class PolicySearchInput(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
    department: Literal["hr", "accounting", "legal"]
    top_k: int = Field(default=3, ge=1, le=8)


def search_department_policies(payload: PolicySearchInput | dict) -> dict:
    if isinstance(payload, dict):
        payload = PolicySearchInput(**payload)

    evidence = retrieve(payload.question, payload.department, payload.top_k)
    return {
        "status": "ok" if evidence else "no_evidence",
        "count": len(evidence),
        "evidence": evidence,
    }
