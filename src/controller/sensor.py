from fastapi import File,UploadFile
import pandas as pd

def calculateSW():
    print("hello")
    
async def read_file(file:UploadFile = File()):
    if file is None:
        return {"Error not found"}
    contest = await file.read()
    df = pd.read_excel(contest)
    heads = list(df.columns)
    x,y = await count_v(heads)
    num_pa = df.shape[0]
    return x,y,num_pa

async def read_file_txt():
    print()    

async def count_v(list:list):
    x = 0
    y = 0
    for index in list:
        print(index)
        x = x + index.count('X')
        y = y + index.count('YD')
    return x,y    

