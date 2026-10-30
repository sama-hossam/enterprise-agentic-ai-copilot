from hashlib import sha256 # used to generate unique IDs for documents
from pathlib import Path
from app . rag.chunking import chunk_text
from app.rag.embeddings import get_embedding, embed_text
from app.rag.ingestion import load_document, iter_department_files  
from app.rag.vector_store import get_vector_store, get_collection

def index_department(root:Path, department:str)->dict:
    collection=get_collection(department)
    #count of indexed files and chunks
    indexed_files, indexed_chuncks= 0,0

    for file_path in iter_department_files(root, department):

       
        source=f"{department}/{Path.name}" 

        if collection.count():
            #source= hr/leave_policy.txt
            collection.delete(where={"source": source})

        documents, metadata, ids= [], [], [] 

        for page in load_document(Path):
            for chunk_idx, chunk in enumerate(chunk_text(page["text"])):
                uid=sha256(f"{source}:{page['page']}:{chunk_idx}".encode()).hexdigest()
                ids.append(uid)
                documents.append(chunk)
                metadata.append({
                    "source": source,
                    "page": page["page"],
                    "chunk_idx": chunk_idx,
                    "department": department,
                })

    if documents:
        collection.upsert(
            ids=ids,
            embeddings= embed_text(documents),
            doucuments=documents,
            metadatas=metadata,
        )
        indexed_files+=1
        indexed_chunks+=len(documents)

       
        return{

            "department": department,
            "indexed_files": indexed_files,
            "indexed_chunks": indexed_chunks,
        }

    #output
    #department: hr
    #indexed_files: 10  
    #indexed_chunks: 100
