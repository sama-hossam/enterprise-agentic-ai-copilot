"""One shared embedding model for all policy departments."""
from functools import lru_cache
from app.core.config import get_settings

@lru_cache(maxsize=1)
def get_embedding_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(get_settings().rag_embedding_model)

def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_embedding_model()
    vectors = model.encode(texts, normalize_embeddings=True)
    return vectors.tolist()
