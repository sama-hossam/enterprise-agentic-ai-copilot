"""Create embeddings for chunks. Placeholder - implemented in Module 8."""
# use cahing to avoid recomputing embeddings for the same text
from functools import lru_cache
from app. core.config import get_settings

@lru_cache(maxsize=1) #decorator use it insted loading the model every time we call the function
#what is maxsize=1? it means we will cache the result of the function for the last 1 call, so if we call the function with the same text again, it will return the cached result instead of recomputing the embedding
#what if i call the function with different text? it will compute the embedding for the new text and cache it, replacing the previous cached result
#what if i return to the previous text? it will compute the embedding again, since the cached result was replaced by the new text
#what if i reset the application? it will clear the cache, so the next time we call the function, it will compute the embedding again

def get_embedding_model():
    from sentence_transformers import SentenceTransformer

    model_name = get_settings().rag.embedding_model_name
    return SentenceTransformer(model_name)

def embed_text(text: list[str]) -> list[list[float]]:

    model = get_embedding_model()
    vector=model.encode(text,normalize_embeddings=True) 
    #normalize matters because it ensures that the embeddings are on the same scale, which can improve the performance of similarity searches and other downstream tasks. Normalization typically involves scaling the embeddings to have a unit norm (length of 1), which helps in comparing the embeddings more effectively.
    #why it is matter to retrival? because when we perform retrieval tasks, we often compute the similarity between embeddings using metrics like cosine similarity. If the embeddings are not normalized, the magnitude of the vectors can affect the similarity scores, leading to less accurate retrieval results. Normalized embeddings ensure that the similarity scores are based solely on the direction of the vectors, which is more meaningful for comparing semantic content.
    #give me example of normalized embeddings? Sure! Let's say we have two text chunks: "I love programming" and "I enjoy coding". After passing them through the embedding model, we might get the following raw embeddings (these are just illustrative numbers): 
    # Raw Embeddings: [0.8, 0.1, 0.2], [0.1, 0.9, 0.3]
    #  what if not normalized? If we don't normalize these embeddings, their magnitudes can vary significantly. For example, the first embedding has a magnitude of sqrt(0.8^2 + 0.1^2 + 0.2^2) ≈ 0.83, while the second embedding has a magnitude of sqrt(0.1^2 + 0.9^2 + 0.3^2) ≈ 0.95. When we compute cosine similarity between these two embeddings, the result will be influenced by their magnitudes, potentially leading to misleading similarity scores. how it is happen? because cosine similarity is calculated as the dot product of the two vectors divided by the product of their magnitudes. If the magnitudes are different, it can skew the similarity score, making it less reliable for comparing semantic content. By normalizing the embeddings, we ensure that both vectors have a magnitude of 1, allowing us to focus solely on their direction and thus providing a more accurate measure of similarity.
    #

    return vector.tolist()