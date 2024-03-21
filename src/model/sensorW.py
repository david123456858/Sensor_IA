from pydantic import BaseModel
from typing import Union

class sensor(BaseModel):
    valueW: list[list[float]] 
    valueU: list[float]
    
    
