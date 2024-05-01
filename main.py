from fastapi import FastAPI,UploadFile,File,Response,status
from fastapi.responses import UJSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd


from src.controller.sensor import read_file,generateWAndU,sensor_data,generateWandUforCapas,read_binary
from src.upload.save_file import data_root
from src.model.sensorW import sensor
from src.model.capas import capas


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
    return {"info":"Bienvenido a nuestro back del sensor"}

## find() // find_one() 

##Conexion a mongoDB para poder extraer los datos 

##Post donde se nos permite traer el archivo de entrenamiento y hacer el debido proceso de inializacion 
@app.post('/file/binary',status_code=200,response_class=UJSONResponse)
async def current_data(res:Response,file:UploadFile= File()):
    if(file):
        res.status_code = status.HTTP_202_ACCEPTED
        await read_binary(file)
        
    
    
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
        return [{ "numEntradas": x,
                  "numSalidas": y,
                  "numPatrones":num_pa,
                  "W":w,
                  "U":u,
                  "cabeceras":cabeceras,
                  "salidas":y_columns.values.tolist(),
                  "entradas":x_columns.values.tolist(),}]
        
@app.post('/simular',status_code=202,response_class=UJSONResponse)
async def recive_file(res:Response,file:UploadFile = File()):
    if(file):
        res.status_code = status.HTTP_202_ACCEPTED
        x,y,num_pa,df = await read_file(file)
        print("df:",df)
        x_columns = df.filter(like='X')
        return [{ "entradas":x_columns.values.tolist() }]
        
##subiendo el arhivo
@app.post("/save",status_code=200,response_class=UJSONResponse)
def saveW_U(values_data:sensor):
    _path = data_root()
    print(_path)
    df = sensor_data(values_data)
    print(df)
    df.to_excel(_path, index=False)
    return { "Los valores se han guardado correctamente" }
      
##Mandando los capas 
@app.post("/capas",status_code=200, response_class=UJSONResponse)
async def file_recive(capas_info:capas,res:Response):
    if(capas_info):
        res.status_code = status.HTTP_202_ACCEPTED
        pesos,umbrales = generateWandUforCapas(capas_info)
        data = {}
        for i, (peso_capa,umbral_capa) in enumerate(zip(pesos,umbrales)):
            data[f"capa{i}"] = {
                "pesos":peso_capa,
                "umbrales":umbral_capa
            }   
        return data

     