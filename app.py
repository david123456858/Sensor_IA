from typing import Union
from fastapi import FastAPI,UploadFile,File,Response,status
from fastapi.responses import UJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.controller.sensor import read_file

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

@app.post('/file/',status_code=202,response_class=UJSONResponse)
async def recive_file(res:Response,file:UploadFile = File()):
    if(file):
        res.status_code = status.HTTP_202_ACCEPTED
        df = await read_file(file)
        print(df.head())

    