"""Retrieve relevant chunks for a query. Placeholder - implemented in Module 8."""
"""Retrieve relevant evidence from the vector database."""

from app.rag.embeddings import embed_texts
from app.rag.vector_store import get_collection


def retrieve(question: str,department: str,top_k: int = 3) -> list[dict]:
  
    if not 1 <= top_k <= 8:
        raise ValueError("top_k must be between 1 and 8")

    collection = get_collection(department)

    if collection.count() == 0:
        return []

    question_embedding = embed_texts([question])

    results = collection.query(
        query_embeddings=question_embedding,
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    evidence = []

    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        evidence.append({
            "text": text,
            "source": metadata["source"],
            "page": metadata["page"],
            "department": department,
            "distance": round(float(distance), 4)
        })

    return evidence