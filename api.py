import numpy as np
import matplotlib.pyplot as plt
import json
import base64
import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from io import BytesIO
from pathlib import Path
from PIL import Image
from typing import Annotated

from models import ReceivedData


def create_folder(directory: Path) -> Path:
    current_time = datetime.datetime.now()
    new_subfolder_name = current_time.strftime("%Y_%m_%d_%H_%M/")
    new_subfolder = Path(f"{directory}/{new_subfolder_name}")
    new_subfolder.mkdir(exist_ok=True)

    return new_subfolder


UPLOAD_DIR = "uploads/"

app: FastAPI = FastAPI()


origins = ["http:127.1.0.0", "http://127.0.0.1:5500"]


# Note: CORS enabled means that the request from the client reach the server but nothing is return -> actions can be executed within a route (problem? how to limit it)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root() -> JSONResponse:

    return JSONResponse(status_code=200, content={"message": "welcome to root"})


@app.post("/upload")
async def upload(request: Request) -> JSONResponse:
    data: bytes = await request.body()

    try:
        deserialized_data = json.loads(data)
        received_data = ReceivedData(
            images=deserialized_data["images"],
            filenames=deserialized_data["filenames"],
            username=deserialized_data["email"].split("@")[0],
        )
    except Exception as e:
        print(f"Received data could not be read - Exception {e} raised")
        return JSONResponse(status_code=400, content={"message": "issue occured"})

    user_folder = Path(f"{UPLOAD_DIR}/{received_data.username}/")
    user_folder.mkdir(exist_ok=True)

    image_folder_path = create_folder(user_folder)

    files = [f for f in Path(image_folder_path).iterdir() if f.is_file()]
    file_counter = len(files)

    for image, filename in zip(received_data.images, received_data.filenames):
        image_bytes = base64.b64decode(image)

        # check quality (lighting and blurring) based on expected historgram
        # if not good, skip image

        file_format = filename.split(".")[1]
        file_counter += 1
        file_path = Path(f"{image_folder_path}/{file_counter}.{file_format}")
        with open(file_path, "wb+") as f:
            try:
                # stores image data in bytes that can be read by e.g., first converting uploaded bytes into BytesIO
                # and then Image.open() for extracting the correspondign image format
                f.write(image_bytes)
                print(f"File {filename} successfully stored")

            except:
                print(f"File {filename} could not be stored")

        """
        img = Image.open(BytesIO(image_bytes))
        plt.imshow(img)
        plt.show()
        """
    return JSONResponse(content={"message": "bytes delivered"})
