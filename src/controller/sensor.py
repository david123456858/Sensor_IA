from fastapi import File,UploadFile
import pandas as pd

def calculateSW():
    print("hello")
    
async def read_file(file:UploadFile = File()):
    if file is None:
        return {"Error not found"}
    contest = await file.read()
    df = pd.read_excel(contest)
    return df
    
async def read_file_txt():
    print()    