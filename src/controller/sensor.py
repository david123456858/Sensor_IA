from fastapi import File,UploadFile
import pandas as pd
import random
from src.model.sensorW import sensor
from src.model.capas import capas

def sensor_data(data:sensor) -> pd.DataFrame:
    print("data", data)
    df_W = pd.DataFrame(data.valueW,columns=[f'W{i}' for i in range(len(data.valueW[0]))]) 
    df_W['U'] = data.valueU
    return df_W
async def read_file(file:UploadFile = File()):
    if file is None:
        return {"Error not found"}
    contest = await file.read()
    df = pd.read_excel(contest)
    print(df)
    heads = list(df.columns)
    x,y = count_v(heads)
    num_pa = df.shape[0]
    return x,y,num_pa,df


async def read_binary(file:UploadFile = File()):
    if file is None:
        return {"Not Found"}
    read = await file.read()
    df = pd.read_excel(read)
    heads = list(df.columns)
    x,y = count_v(heads)
    
    print(read)
    
def changePropery(banco:pd.DataFrame) -> pd.DataFrame:
    
    print(banco)
    
##contador de las entradas y salidas
def count_v(list:list)-> any:
    x = 0
    y = 0
    for index in list:
        # print(index)
        x = x + index.count('X')
        y = y + index.count('YD')
    return x,y   

##Generando los pesos y umbrales 
def generateWAndU(x,y) :
    w = [[round(random.uniform(0,1), 1) for _ in range(y)]for _ in range(x)]
    u = [round(random.uniform(-1,1),1) for _ in range(y)]
    return w,u

def generateWAndUBack(x,y) :
    w = [[round(random.uniform(0,1), 1) for _ in range(y)]for _ in range(x)]
    u = [round(random.uniform(-1,1),1) for _ in range(y)]
    return w,u
def saveValues(data:sensor):
    dfW = pd.DataFrame(data.valueW)
    dfU = pd.DataFrame(data.valueU)
    dfW.columns = ["W1","W2"]
    dfU.columns = ["U"]
    return dfW,dfU

def generateWandUforCapas(data:capas):
    weights = []
    biases = []
    for i in range(len(data.numNeu)):
        if i == 0:  # Para la primera capa
            # Generar matriz de pesos y vector de sesgo
            w, u = generateWAndUBack(data.x, data.numNeu[i])
            weights.append(w)
            biases.append(u)
            if(len(data.numNeu) == 1):
                ##si solo hay una capa, entonces solo hay necesidad de tener dos pesos y salirme 
                w,u = generateWAndUBack(data.numNeu[i], data.y)
                weights.append(w)
                biases.append(u)
                return
            
        elif i < len(data.numNeu) - 1:  # Para las capas intermedias
            # Cunando toca en una capa intermedia toca evaluar la actual y la anterior pero tambien verificar 
            w, u = generateWAndUBack(data.numNeu[i-1], data.numNeu[i])
            weights.append(w)
            biases.append(u)
            
        else:  # Para la última capa
            
            w,u = generateWAndUBack(data.numNeu[i-1], data.numNeu[i])
            weights.append(w)
            biases.append(u)
            # Generar matriz de pesos y vector de sesgo
            w, u = generateWAndUBack(data.numNeu[i], data.y)
            weights.append(w)
            biases.append(u)
            
    
    return weights, biases
    
