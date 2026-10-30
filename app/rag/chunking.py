"""Split documents into chunks. Placeholder - implemented in Module 8."""


#return type hint for the function 
def chunk_text(text:str, chunk_size:int =450,overlap:int =50)->list[str]:

    if not 0<=overlap <chunk_size:
        raise ValueError("Overlap must be non-negative and less than chunk size")
    
    text =" ".join(text.split())
    chunks =[]


    #sliding window     start end      step=450-90=360
    for start in range (0,len(text),chunk_size-overlap):#paragrph =450

        piece =text[start:start+chunk_size]
        if piece:
            chunks.append(piece)

        #stop if the next start index would exceed the text length    
        if start + chunk_size >= len(text):
            break    
    return chunks