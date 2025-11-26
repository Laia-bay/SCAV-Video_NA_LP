from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import Response
from PIL import Image
import numpy as np
import os
from first_seminar import colors, resizing, serpentine_pattern, black_white, RLE, DCT, DWT

app = FastAPI()

IMAGE_FOLDER = "images"
RESULT_FOLDER = "result_images"

os.makedirs(RESULT_FOLDER, exist_ok=True)
@app.post("/serpentine")
async def serpentine_endpoint(file: UploadFile = File(...)):
    img_bytes = await file.read()

    input_path = "temp_input.jpg"
    output_path = "result_images/output_serpentine.jpg"

    with open(input_path, "wb") as f:
        f.write(img_bytes)

    serpentine_pattern.serpentine(input_path, output_path)

    with open(output_path, "rb") as f:
        return Response(content=f.read(), media_type="image/jpeg")


@app.post("/B&W")
async def bw_endpoint(file: UploadFile = File(...)):
    img_bytes = await file.read()

    input_path = "temp_input.jpg"
    output_path = "result_images/output_bw.jpg"

    with open(input_path, "wb") as f:
        f.write(img_bytes)

    black_white.grayscale_image(input_path, output_path)

    with open(output_path, "rb") as f:
        return Response(content=f.read(), media_type="image/jpeg")