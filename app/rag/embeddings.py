"""Create embeddings for chunks. Placeholder - implemented in Module 8."""
from functools import lru_cache
from app. core.config import get_settings

@lru_cache(maxsize=1) 
def get_embedding_model():
    from sentence_transformers import SentenceTransformer

    model_name = get_settings().rag.embedding_model_name
    return SentenceTransformer(model_name)

def embed_text(text: list[str]) -> list[list[float]]:

    model = get_embedding_model()
    vector=model.encode(text,normalize_embeddings=True) 
   

    return vector.tolist()
