from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import Response
from PIL import Image
import numpy as np
import os
from first_seminar import colors, resizing, serpentine_pattern, black_white, RLE, DCT, DWT
import ffmpeg

app = FastAPI()

IMAGE_FOLDER = "images"
RESULT_FOLDER = "result_images"

os.makedirs(RESULT_FOLDER, exist_ok=True)   ## to make sure that the folder where the modified images will be saved exists.


@app.post("/serpentine")
async def serpentine_endpoint(file: UploadFile = File(...)):
    img_bytes = await file.read()

    input_path = "temp_input.jpg"
    output_path = "result_images/output_serpentine.jpg"

    with open(input_path, "wb") as f:
        f.write(img_bytes)

    serpentine_pattern.serpentine(input_path, output_path)

    with open(output_path, "rb") as f:
        return Response(content=f.read(), media_type="image/jpg")


@app.post("/B&W")
async def bw_endpoint(file: UploadFile = File(...)):
    img_bytes = await file.read()

    input_path = "temp_input.jpg"
    output_path = "result_images/output_bw.jpg"

    with open(input_path, "wb") as f:
        f.write(img_bytes)

    black_white.grayscale_image(input_path, output_path)

    with open(output_path, "rb") as f:
        return Response(content=f.read(), media_type="image/jpg")
    

@app.post("/resize_video")
async def resize_video_endpoint(file: UploadFile = File(...)):
    img_bytes = await file.read()

    input_path = "temp_input.mp4"
    output_path = "image_results/resized_video.mp4"

    with open(input_path, "wb") as f:
        f.write(img_bytes)
    
    ffmpeg.input(input_path).output(output_path, vf=f"scale={1280/2}:{720/2}").run(capture_stdout=True, capture_stderr=True, overwrite_output=True)

    with open(output_path, "rb") as f:
        return Response(content=f.read(), media_type="video/mp4")