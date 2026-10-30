"""Vector DB wrapper (e.g. ChromaDB). Placeholder - implemented in Module 8."""
from functools import lru_cache
from pathlib import Path
from app.core.config import get_settings

DEPARTMENT={"hr", "accounting", "legal","it"}

#save the connection
@lru_cache(maxsize=1)
def get_vector_store():
    #import inside to avoid circular import issues if cachw is used
    import chromadb
    #get the path from the config file to store the vector database
    store= Path(get_settings().rag_croma_path)
    #create the directory if it does not exist 
    store.mkdir(parents=True,exist_ok=True)
    #
    return chromadb.PersistentClient(path=str(store))

 
def get_collection(department:str):
    if department not in DEPARTMENT:
        raise ValueError(f"Unsupported department: {department}")
    #get the vector store connection
    store=get_vector_store()
    #get the collection for the department, create if it does not exist
    return store.get_or_create_collection(name=department, metadata={"hnsw:space": "cosine"})