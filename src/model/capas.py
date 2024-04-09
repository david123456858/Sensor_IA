from pydantic import BaseModel


class capas(BaseModel):
    capas:int
    x:int
    y:int
    numNeu:list[int]