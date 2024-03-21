from fastapi import FastAPI,UploadFile,File,Response,status
from fastapi.responses import UJSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from src.controller.sensor import read_file,generateWAndU


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

@app.get('/hola')
def hello():
    return {"acuña mmaguevo"}

@app.get('/')
def read_root():
    return {"Hello": "Word"}

##Post donde se nos permite traer el archivo de entrenamiento y hacer el debido proceso de inializacion 
@app.post('/file',status_code=202,response_class=UJSONResponse)
async def recive_file(res:Response,file:UploadFile = File()):
    print("entre")
    if(file):
        res.status_code = status.HTTP_202_ACCEPTED
        x,y,num_pa,df = await read_file(file)
        cabeceras = df.columns.to_list()
        print("df:",df)
        x_columns = df.filter(like='X')
        y_columns = df.filter(like='Y')
        print(x_columns)
        print(y_columns)
        valores = df.values.tolist()
        print(valores)
        w,u = generateWAndU(x,y)
        return [{ "entradas": x,
                  "salidas": y,
                  "patrones":num_pa,
                  "W":w,
                  "U":u,
                  "cabeceras":cabeceras,
                
                  "valores":valores,
                  "valoresSalidas":y_columns.values.tolist(),
                  "valoresEntradas":x_columns.values.tolist(),}]


     