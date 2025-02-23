from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
from typing import Annotated
import matplotlib.pyplot as plt 
import shutil
from PIL import Image
from io import BytesIO
import os
import json
import base64
import datetime
from pathlib import Path


UPLOAD_DIR = "uploads/"

app: FastAPI = FastAPI()




origins = [
    "http:127.1.0.0", "http://127.0.0.1:5500"
]


# Note: CORS enabled means that the request from the client reach the server but nothing is return -> actions can be executed within a route (problem? how to limit it)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def read_root()-> dict:
    print("root path accessed")

    return {"message": f"welcome"}


    
@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    print(file.file)

    
    with open(file.file, "wb") as f:
        cont_open = f.read()
        print("Cont open:", cont_open)


    contents = file.file.read() # reads data as vytest
    print("Contents", contents)
    try:

        upload_dir = "uploads/"
        file_path = upload_dir + file.filename

        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        return JSONResponse(content={"message": "File upload successful", "filename": file.filename})    

    except Exception as e:
        return JSONResponse(status_code=400, content={"detail":str(e)})
        



@app.post("/upload")
async def upload(request: Request):
    data: bytes = await request.body()

    try:
        data_decoded = json.loads(data)
        images = data_decoded["images"]
        filenames = data_decoded["filenames"]
        user_name = data_decoded["email"].split("@")[0]
    except AttributeError as e:
        print("Attribute error:", str(e))
    except Exception as e:
        print(f"Received data could not be read - Exception {e} raised")
        return JSONResponse(status_code=400, content={"message": "issue occured"})



    user_folder = Path(f'{UPLOAD_DIR}/{user_name}/')
    user_folder.mkdir(exist_ok=True)

    current_time = datetime.datetime.now()
    new_subfolder = current_time.strftime('%Y_%m_%d_%H_%M/')
    image_folder_path = Path(f"{user_folder}/{new_subfolder}")
    image_folder_path.mkdir(exist_ok=True)

    files = [f for f in Path(image_folder_path).iterdir() if f.is_file()]
    file_counter = len(files)

    for image, filename in zip(images, filenames):
        image_bytes = base64.b64decode(image)
        file_format = filename.split(".")[1]
        file_counter += 1 
        file_path = Path(f'{image_folder_path}/{file_counter}.{file_format}')
        with open(file_path, "wb+") as f:
            print("Writing received data to file")
            # stores image data in bytes that can be read by e.g., first converting uploaded bytes into BytesIO 
            # and then Image.open() for extracting the correspondign image format
            f.write(image_bytes) 


        img = Image.open(BytesIO(image_bytes))
        plt.imshow(img)
        plt.show()
    
    return JSONResponse(content={"message": "bytes delivered"})
    



