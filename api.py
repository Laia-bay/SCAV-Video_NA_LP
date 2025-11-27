from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import Response, JSONResponse
from PIL import Image
import numpy as np
import os
from first_seminar import colors, resizing, serpentine_pattern, black_white, RLE, DCT, DWT
import ffmpeg

app = FastAPI()

IMAGE_FOLDER = "images"
RESULT_FOLDER = "image_results"

os.makedirs(RESULT_FOLDER, exist_ok=True)   ## to make sure that the folder where the modified images will be saved exists.


@app.post("/serpentine")
async def serpentine_endpoint(file: UploadFile = File(...)):
    img_bytes = await file.read()

    input_path = "images/temp_input.jpg"
    output_path = "image_results/output_serpentine.jpg"

    with open(input_path, "wb") as f:
        f.write(img_bytes)

    serpentine_pattern.serpentine(input_path, output_path)

    with open(output_path, "rb") as f:
        return Response(content=f.read(), media_type="image/jpg")


@app.post("/B&W")
async def bw_endpoint(file: UploadFile = File(...)):
    img_bytes = await file.read()

    input_path = "images/temp_input.jpg"
    output_path = "image_results/output_bw.jpg"

    with open(input_path, "wb") as f:
        f.write(img_bytes)

    black_white.grayscale_image(input_path, output_path)

    with open(output_path, "rb") as f:
        return Response(content=f.read(), media_type="image/jpg")
    

@app.post("/resize_video")
async def resize_video_endpoint(file: UploadFile = File(...)):
    img_bytes = await file.read()

    input_path = "images/temp_input.mp4"
    output_path = "image_results/resized_video.mp4"

    with open(input_path, "wb") as f:
        f.write(img_bytes)
    
    ffmpeg.input(input_path).output(output_path, vf=f"scale={1280/2}:{720/2}").run(capture_stdout=True, capture_stderr=True, overwrite_output=True)

    with open(output_path, "rb") as f:
        return Response(content=f.read(), media_type="video/mp4")

# Endpoint to modify the chroma subsampling 
@app.post("/chroma_subsampling")
async def chroma_subsampling(file: UploadFile = File(...)):

    img_bytes = await file.read()

    input_path = "images/temp_chroma_subsampling_input.jpg"
    output_path = "image_results/test_chroma_subsampling.jpg"

    with open(input_path, "wb") as f:
        f.write(img_bytes)

    # Apply chroma subsampling using pix_fmt
    ffmpeg.input(input_path).output(output_path, pix_fmt="yuvj420p").run(capture_stdout=True, capture_stderr=True, overwrite_output=True)

    with open(output_path, "rb") as f:
        return Response(content=f.read(), media_type="image/jpg")

# Endpoint to read the video info and print at least 5 relevant data from the video 
@app.post("/video_info")
async def video_info(file: UploadFile = File(...)):
    video_bytes = await file.read()

    input_path = "images/temp_video_info_input.mp4"

    with open(input_path, "wb") as f:
        f.write(video_bytes)

    # ffprobe command to extract all possible metadata from the media file 
    metadata = ffmpeg.probe(input_path)["streams"]

    return JSONResponse(content=metadata)