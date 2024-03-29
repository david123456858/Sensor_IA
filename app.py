from fastapi import FastAPI,UploadFile,File,Response,status
from fastapi.responses import UJSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

from src.controller.sensor import read_file,generateWAndU,saveValues
from src.upload.save_file import data_root
from src.model.sensorW import sensor


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)


@app.get('/')
def read_root():
    return {"info":"Bienvenido a nuestrp back del sensor"}

##Post donde se nos permite traer el archivo de entrenamiento y hacer el debido proceso de inializacion 
@app.post('/file',status_code=202,response_class=UJSONResponse)
async def recive_file(res:Response,file:UploadFile = File()):
    if(file):
        res.status_code = status.HTTP_202_ACCEPTED
        x,y,num_pa,df = await read_file(file)
        cabeceras = df.columns.to_list()
        print("df:",df)
        x_columns = df.filter(like='X')
        y_columns = df.filter(like='Y')
        w,u = generateWAndU(x,y)
        return [{ "entradas": x,
                  "salidas": y,
                  "patrones":num_pa,
                  "W":w,
                  "U":u,
                  "cabeceras":cabeceras,
                  "valoresSalidas":y_columns.values.tolist(),
                  "valoresEntradas":x_columns.values.tolist(),}]

##subiendo el arhivo
@app.post("/save",status_code=200,response_class=UJSONResponse)
def saveW_U(values_data:sensor):
    _path = data_root()
    print(_path)
    dfW,dfU = saveValues(values_data)
    with pd.ExcelWriter(_path) as writer:
        dfW.to_excel(writer,sheet_name='Hoja1', index=False)
        dfU.to_excel(writer,sheet_name='Hoja2',index=False)
    return {"Los valores se han guardado correctamente"}
      