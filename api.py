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
async def chroma_subsampling_endpoint(file: UploadFile = File(...)):

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
async def video_info_endpoint(file: UploadFile = File(...)):
    video_bytes = await file.read()

    input_path = "images/temp_video_info_input.mp4"

    with open(input_path, "wb") as f:
        f.write(video_bytes)

    # ffprobe command to extract all possible metadata from the media file 
    metadata = ffmpeg.probe(input_path)["streams"]

    return JSONResponse(content=metadata)

@app.post("/create_BBB_container")
async def create_BBB_container_endpoint(file: UploadFile = File(...)):
    video_bytes = await file.read()

    input_path = "images/temp_bbb_input.mp4"
    trimmed_video_path = "temp_bbb_trimmed.mp4"
    aac_audio_path = "aac_mono_audio.aac"
    mp3_audio_path = "mp3_stereo_audio.mp3"
    ac3_audio_path = "ac3_audio.ac3"
    output_path = "image_results/test_BBB_container.mp4"

    with open(input_path, "wb") as f:
        f.write(video_bytes)

    # cut first 20 seconds of the video
    ffmpeg.input(input_path).output(trimmed_video_path,t=20,vcodec="libx264").run(overwrite_output=True, capture_stdout=True, capture_stderr=True)

    # create AAC mono audio
    ffmpeg.input(trimmed_video_path).output(aac_audio_path,acodec="aac",ac=1).run(overwrite_output=True, capture_stdout=True, capture_stderr=True)

    # create MP3 stereo audio with lower bitrate
    # initial bitrate = 208216 bps (we obtained this value using the previous endpoint that showed the data of the video)
    ffmpeg.input(trimmed_video_path).output(mp3_audio_path,acodec="mp3",ac=2,audio_bitrate="128k").run(capture_stdout=True, capture_stderr=True, overwrite_output=True)
    
    # create AC3 mono audio
    ffmpeg.input(trimmed_video_path).output(ac3_audio_path,acodec="ac3",ac=2).run(capture_stdout=True, capture_stderr=True, overwrite_output=True)

    # package everything into a single MP4 container
    video_input = ffmpeg.input(trimmed_video_path)
    aac_input = ffmpeg.input(aac_audio_path)
    mp3_input = ffmpeg.input(mp3_audio_path)
    ac3_input = ffmpeg.input(ac3_audio_path)

    ffmpeg.output(
        video_input, aac_input, mp3_input, ac3_input,
        output_path,
        vcodec="copy",
        acodec="copy",
    ).run(capture_stdout=True, capture_stderr=True, overwrite_output=True)

    with open(output_path, "rb") as f:
        return Response(content=f.read(), media_type="video/mp4")
    
# Endpoint to inspect mp4 tracks 
@app.post("/inspect_mp4_tracks")
async def inspect_mp4_tracks_endpoint(file: UploadFile = File(...)):
    video_bytes = await file.read()

    input_path = "images/temp_container_mp4"

    with open(input_path, "wb") as f:
        f.write(video_bytes)

    probe = ffmpeg.probe(input_path)

    video_tracks = [s for s in probe["streams"] if s["codec_type"] == "video"]
    audio_tracks = [s for s in probe["streams"] if s["codec_type"] == "audio"]

    return {"total_tracks": len(probe["streams"]),"video_tracks": len(video_tracks),"audio_tracks": len(audio_tracks)}

# Endpoint to show the macroblocks and the motion vectors 
@app.post("/macroblocks_motion_vectors")
async def macroblocks_motion_vectors_endpoint(file: UploadFile = File(...)):
    video_bytes = await file.read()

    input_path = "images/temp_input_mp4"
    output_path = "image_results/test_macroblocks_motion_vectors.mp4"

    with open(input_path, "wb") as f:
        f.write(video_bytes)

    ffmpeg.input(input_path,flags2="+export_mvs").output(output_path,vf="codecview=mv=pf+bf+bb").run(capture_stdout=True, capture_stderr=True, overwrite_output=True)

    with open(output_path, "rb") as f:
        return Response(content=f.read(), media_type="video/mp4") 
    
# Endpoint to show the YUV histogram
@app.post("/yuv_histrogram")
async def yuv_histogram_endpoint(file: UploadFile = File(...)):
    video_bytes = await file.read()

    input_path = "images/temp_input_mp4"
    output_path = "image_results/test_yuv_histogram.mp4"

    with open(input_path, "wb") as f:
        f.write(video_bytes)

    ffmpeg.input(input_path).output(output_path,vf="histogram").run(capture_stdout=True, capture_stderr=True, overwrite_output=True)

    with open(output_path, "rb") as f:
        return Response(content=f.read(), media_type="video/mp4") 