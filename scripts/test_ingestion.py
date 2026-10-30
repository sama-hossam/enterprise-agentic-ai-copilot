import sys
from pathlib import Path #the best to deal with many paths avoide the conflicts of / or\

root_dir=Path(__file__).resolve().parents[1]
sys.path.append(str(root_dir))


from app.rag.ingestion import load_document, iter_department_files

def main():
    data_dir=root_dir/"data"/"raw"
    print ("Testing Iter Department Files For HR")

    hr_files=list(iter_department_files(data_dir,"it"))
    for f in hr_files:
        print (f"Found:{f.name}")

    if hr_files:
        print("\n Testing load document ")
        docs= load_document(hr_files[0])
        if docs:
            print(f"page number: {docs[0]['page']}")
            print(f"ptext: {docs[0]['text'][:150]}")


if __name__=="__main__":
    main()
            
    