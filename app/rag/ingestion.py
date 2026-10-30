"""Load documents from data/raw. Placeholder - implemented in Module 8."""
"""Read local policy documents. These are synthetic training documents."""
from pathlib import Path

SUPPORTED = {".txt", ".md", ".pdf"}
#file_path=path("D:\enterprise-agentic-ai-copilot\data\raw\hr\leave_policy.text")


'''def load_document (file_path: path):
    #if path does not exist
    if not file_path .exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    #if path is not a file
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    
    
    if file_path.suffix.lower()!=".text":
        raise ValueError(f"Unsupported file type: {file_path.suffix}. Only .txt files are supported.")
    
    text= file_path.read_text(encoding="utf-8")#utf-8 to be able to read all the characters in the text file, including special characters and non-ASCII characters
     #metadata about doc will be needed for retrival stage
    document ={
         "content": text,
         "source": str(file_path),
         "department": file_path.parent.name,
         "file_type": file_path.suffix.lower(),
     }
    return document'''

def load_document(path: Path) -> list[dict]:
    if path.suffix.lower() not in SUPPORTED:
        return []
    if path.suffix.lower() == ".pdf":
        import fitz  # installed by pymupdf; supports text-based PDFs
        with fitz.open(path) as pdf:
            pages = [{"page": index + 1, "text": page.get_text()}
                     for index, page in enumerate(pdf)]
        return [p for p in pages if p["text"].strip()]
    text = path.read_text(encoding="utf-8")
    return [{"page": 1, "text": text}] if text.strip() else []


def iter_department_files(root: Path, department: str):
    if department not in {"hr", "accounting", "legal","it"}:
        raise ValueError("Unsupported department")
    folder = root / department
    if not folder.is_dir():
        return
    # yield return object generator 
    yield from sorted(p for p in folder.iterdir() # read the folder content 
                      if p.is_file() and p.suffix.lower() in SUPPORTED)
