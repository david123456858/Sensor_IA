from fastapi import File,UploadFile
import pandas as pd
import random

def calculateSW():
    print("hello")
    
async def read_file(file:UploadFile = File()):
    if file is None:
        return {"Error not found"}
    contest = await file.read()
    df = pd.read_excel(contest)
    heads = list(df.columns)
    x,y = count_v(heads)
    num_pa = df.shape[0]
    return x,y,num_pa,df

async def read_file_txt():
    print()    
    
##contador de las entradas y salidas
def count_v(list:list):
    x = 0
    y = 0
    for index in list:
        print(index)
        x = x + index.count('X')
        y = y + index.count('YD')
    return x,y   

##Generando los pesos y umbrales 
def generateWAndU(x,y):
    w = [[round(random.uniform(0,1), 1) for _ in range(y)]for _ in range(x)]
    ##print(w)
    u = [round(random.uniform(-1,1),1) for _ in range(y)]
    ##print(u)
    return w,u


