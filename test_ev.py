from typing import Literal # to define a variable that can only take a specific set of values
#                          Field   allaw to add constraints on massage longth
from pydantic import BaseModel, Field, ValidationError

class AskRequest(BaseModel):
    question: str=Field(min_Length=3,max_length=1000)
    department: Literal["hr", "accounting", "legal"] 
    #top_k for the number of top documents to retrieve
    top_k: int=Field(default=3, ge=1, le=8) # default value is 3, must be between 1 and 8 inclusive 


bad_data={"question":"Hi",
          "department":"sales",
          "top_k":50}
print ("bad_data")

try:
    req=AskRequest(**bad_data)
except ValidationError as e:
    print("request rejected",e.json())