"""Persistent Chroma collections, with one collection per department."""
from functools import lru_cache
from pathlib import Path
from app.core.config import get_settings

DEPARTMENTS = {"hr", "accounting", "legal"}

@lru_cache(maxsize=1)
def get_client():
    import chromadb
    store = Path(get_settings().rag_chroma_path)
    store.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(store))

def get_collection(department: str):
    if department not in DEPARTMENTS:
        raise ValueError("Unsupported department")
    return get_client().get_or_create_collection(
        name=f"depi_policies_{department}",
        metadata={"hnsw:space": "cosine"},
    )
