from typing import Union
from fastapi import FastAPI,UploadFile,File,Response,status
from fastapi.responses import UJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.controller.sensor import read_file,generateWAndU

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
    return {"Hello": "Word"}

##Post donde se nos permite traer el archivo de entrenamiento y hacer el debido proceso de inializacion 
@app.post('/file/',status_code=202,response_class=UJSONResponse)
async def recive_file(res:Response,file:UploadFile = File()):
    if(file):
        res.status_code = status.HTTP_202_ACCEPTED
        x,y,num_pa = await read_file(file)
        w,u = generateWAndU(x,y)
        return [{"x": x,"y": y,"patr":num_pa,"W":w,"U":u}]


     