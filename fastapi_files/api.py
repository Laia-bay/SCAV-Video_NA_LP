from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Query
from fastapi.responses import Response, JSONResponse
from PIL import Image
import numpy as np
import os
from fastapi_files.first_seminar import colors, resizing, serpentine_pattern, black_white, RLE, DCT, DWT
import ffmpeg

app = FastAPI()

IMAGE_FOLDER = "images"
RESULT_FOLDER = "image_results"
RESULT_VIDEO_FOLDER = "video_results"

os.makedirs(RESULT_FOLDER, exist_ok=True)
os.makedirs(RESULT_VIDEO_FOLDER, exist_ok=True)

@app.post("/rgb2yuv")
async def rgb2yuv_endpoint(r: float = Form(...), g: float = Form(...), b: float = Form(...)):
    rgb = [r, g, b]
    yuv = colors.rgb2yuv(rgb)
    return {"Y": yuv[0], "U": yuv[1], "V": yuv[2]}

@app.post("/yuv2rgb")
async def yuv2rgb_endpoint(Y: float = Form(...), U: float = Form(...), V: float = Form(...)):
    yuv = [Y, U, V]
    rgb = colors.yuv2rgb(yuv)
    return {"R": rgb[0], "G": rgb[1], "B": rgb[2]}

@app.post("/resize_image")
async def resize_image_endpoint(
    file: UploadFile = File(...),
    width: int = Form(...),
    height: int = Form(...)
):
    img_bytes = await file.read()
    input_path = "images/temp_resize_input.jpg"
    output_path = "image_results/output_resized_image.jpg"

    with open(input_path, "wb") as f:
        f.write(img_bytes)

    resizing.resize_image(input_path, output_path, width, height)
    os.remove(input_path)

    with open(output_path, "rb") as f:
        return Response(content=f.read(), media_type="image/jpg")

@app.post("/rle")
async def rle_endpoint(datastream: str = Form(...)):
    rle = RLE.run_length_encoding(str(datastream))
    return {"RLE-applied": rle}

@app.post("/serpentine")
async def serpentine_endpoint(file: UploadFile = File(...)):
    img_bytes = await file.read()
    input_path = "images/temp_input.jpg"
    output_path = "image_results/output_serpentine.jpg"

    with open(input_path, "wb") as f:
        f.write(img_bytes)

    serpentine_pattern.serpentine(input_path, output_path)
    os.remove(input_path)

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
    os.remove(input_path)

    with open(output_path, "rb") as f:
        return Response(content=f.read(), media_type="image/jpg")

@app.post("/resize_video")
async def resize_video_endpoint(file: UploadFile = File(...), width: int = Form(...), height: int = Form(...)):
    video_bytes = await file.read()
    input_path = "images/temp_input.mp4"
    output_path = "video_results/output_resized_video.mp4"

    with open(input_path, "wb") as f:
        f.write(video_bytes)

    if width >= 1080 or height >= 720:
        raise HTTPException(
            status_code=400,
            detail="Size must be smaller than original:1280x720."
        )
    else:
        ffmpeg.input(input_path).output(output_path, vf=f"scale={width}:{height}").run(
            capture_stdout=True, capture_stderr=True, overwrite_output=True
        )

    os.remove(input_path)

    with open(output_path, "rb") as f:
        return Response(content=f.read(), media_type="video/mp4")

@app.post("/chroma_subsampling")
async def chroma_subsampling_endpoint(file: UploadFile = File(...), subsampling: str = Form(...)):
    video_bytes = await file.read()
    input_path = os.path.join(IMAGE_FOLDER, "temp_chroma_subsampling_input.jpg")
    output_path = os.path.join(RESULT_FOLDER, "output_chroma_subsampling.jpg")

    with open(input_path, "wb") as f:
        f.write(video_bytes)

    ffmpeg.input(input_path).output(output_path, pix_fmt=f"yuv{subsampling}p").run(
        capture_stdout=True, capture_stderr=True, overwrite_output=True
    )
    os.remove(input_path)

    with open(output_path, "rb") as f:
        return Response(content=f.read(), media_type="image/jpg")

@app.post("/video_info")
async def video_info_endpoint(file: UploadFile = File(...)):
    video_bytes = await file.read()
    input_path = os.path.join(IMAGE_FOLDER, "temp_video_info_input.mp4")

    with open(input_path, "wb") as f:
        f.write(video_bytes)

    metadata = ffmpeg.probe(input_path)["streams"]
    video_stream = metadata[0]
    audio_stream = metadata[1]

    five_data = {
        "video_codec_name": video_stream.get("codec_name"),
        "audio_codec_name": audio_stream.get("codec_name"),
        "resolution": f"{video_stream.get('width')}x{video_stream.get('height')}",
        "duration": video_stream.get("duration"),
        "frame_rate": video_stream.get("r_frame_rate"),
        "chroma_subsampling": video_stream.get("pix_fmt")
    }

    os.remove(input_path)
    return JSONResponse(content=five_data)

@app.post("/create_BBB_container")
async def create_BBB_container_endpoint(file: UploadFile = File(...), AAC_audio: bool = Form(...), MP3_audio: bool = Form(...), AC3_audio: bool = Form(...)):
    video_bytes = await file.read()
    input_path = os.path.join(IMAGE_FOLDER, "temp_bbb_input.mp4")
    trimmed_video_path = os.path.join(RESULT_VIDEO_FOLDER, "temp_bbb_trimmed.mp4")
    aac_audio_path = os.path.join(RESULT_VIDEO_FOLDER, "aac_mono_audio.aac")
    mp3_audio_path = os.path.join(RESULT_VIDEO_FOLDER, "mp3_stereo_audio.mp3")
    ac3_audio_path = os.path.join(RESULT_VIDEO_FOLDER, "ac3_audio.ac3")
    output_path = os.path.join(RESULT_VIDEO_FOLDER, "output_BBB_container.mp4")

    with open(input_path, "wb") as f:
        f.write(video_bytes)

    ffmpeg.input(input_path).output(trimmed_video_path, t=20, vcodec="libx264", acodec="copy").run(
        overwrite_output=True, capture_stdout=True, capture_stderr=True
    )

    audio_tracks = []

    if AAC_audio:
        ffmpeg.input(trimmed_video_path).output(aac_audio_path, acodec="aac", ac=1).run(overwrite_output=True)
        audio_tracks.append(aac_audio_path)
    if MP3_audio:
        ffmpeg.input(trimmed_video_path).output(mp3_audio_path, acodec="mp3", ac=2).run(overwrite_output=True)
        audio_tracks.append(mp3_audio_path)
    if AC3_audio:
        ffmpeg.input(trimmed_video_path).output(ac3_audio_path, acodec="ac3", ac=2).run(overwrite_output=True)
        audio_tracks.append(ac3_audio_path)

    if not audio_tracks:
        return JSONResponse({"ERROR": "Select at least ONE audio track"}, status_code=400)

    video_input = ffmpeg.input(trimmed_video_path)
    audio_inputs =[ffmpeg.input(a) for a in audio_tracks]

    ffmpeg.output(video_input, audio_inputs, vcodec="copy", acodec="copy").run(overwrite_output=True)

    os.remove(input_path)

    with open(output_path, "rb") as f:
        return Response(content=f.read(), media_type="video/mp4")

@app.post("/inspect_mp4_tracks")
async def inspect_mp4_tracks_endpoint(file: UploadFile = File(...)):
    video_bytes = await file.read()
    input_path = os.path.join(IMAGE_FOLDER, "temp_container_mp4")

    with open(input_path, "wb") as f:
        f.write(video_bytes)

    probe = ffmpeg.probe(input_path)
    video_tracks = [s for s in probe["streams"] if s["codec_type"] == "video"]
    audio_tracks = [s for s in probe["streams"] if s["codec_type"] == "audio"]

    os.remove(input_path)
    return {"total_tracks": len(probe["streams"]), "video_tracks": len(video_tracks), "audio_tracks": len(audio_tracks)}

@app.post("/macroblocks_motion_vectors")
async def macroblocks_motion_vectors_endpoint(file: UploadFile = File(...)):
    video_bytes = await file.read()
    input_path = os.path.join(IMAGE_FOLDER, "temp_input_mp4")
    output_path = os.path.join(RESULT_VIDEO_FOLDER, "output_test_macroblocks_motion_vectors.mp4")

    with open(input_path, "wb") as f:
        f.write(video_bytes)

    ffmpeg.input(input_path, flags2="+export_mvs").output(output_path, vf="codecview=mv=pf+bf+bb").run(
        capture_stdout=True, capture_stderr=True, overwrite_output=True
    )

    os.remove(input_path)
    with open(output_path, "rb") as f:
        return Response(content=f.read(), media_type="video/mp4")

@app.post("/yuv_histogram")
async def yuv_histogram_endpoint(file: UploadFile = File(...)):
    video_bytes = await file.read()
    input_path = os.path.join(IMAGE_FOLDER, "temp_input.mp4")
    output_path = os.path.join(RESULT_VIDEO_FOLDER, "output_test_yuv_histogram.mp4")

    with open(input_path, "wb") as f:
        f.write(video_bytes)

    ffmpeg.input(input_path).output(output_path, vf="histogram", vcodec="libx264", pix_fmt="yuv420p").run(
        capture_stdout=True, capture_stderr=True, overwrite_output=True
    )

    os.remove(input_path)
    with open(output_path, "rb") as f:
        return Response(content=f.read(), media_type="video/mp4")

@app.post("/convert_video_format")
async def convert_video_format_endpoint(file: UploadFile = File(...), VP8: bool = Form(...), VP9: bool = Form(...), h265: bool = Form(...), AV1: bool = Form(...)):
    video_bytes = await file.read()
    input_path = os.path.join(IMAGE_FOLDER, "temp_input.mp4")
    output_vp8_path = os.path.join(RESULT_VIDEO_FOLDER, "output_convert_vp8.webm")
    output_vp9_path = os.path.join(RESULT_VIDEO_FOLDER, "output_convert_vp9.webm")
    output_h265_path = os.path.join(RESULT_VIDEO_FOLDER, "output_convert_h265.mp4")
    output_av1_path = os.path.join(RESULT_VIDEO_FOLDER, "output_convert_av1.mp4")

    with open(input_path, "wb") as f:
        f.write(video_bytes)

    conversions = []

    if VP8:
        stream = ffmpeg.input(input_path)
        stream = ffmpeg.output(stream, output_vp8_path, vcodec="vp8", acodec="libvorbis", **{"q:v": 20})
        ffmpeg.run(stream, capture_stdout=True, capture_stderr=True, overwrite_output=True)
        conversions.append(output_vp8_path)
    if VP9:
        stream = ffmpeg.input(input_path)
        stream = ffmpeg.output(stream, output_vp9_path, vcodec="vp9", acodec="libvorbis", **{"q:v": 20})
        ffmpeg.run(stream, capture_stdout=True, capture_stderr=True, overwrite_output=True)
        conversions.append(output_vp9_path)
    if h265:
        stream = ffmpeg.input(input_path)
        stream = ffmpeg.output(stream, output_h265_path, vcodec="libx265", acodec="aac", **{"q:v": 20})
        ffmpeg.run(stream, capture_stdout=True, capture_stderr=True, overwrite_output=True)
        conversions.append(output_h265_path)
    if AV1:
        stream = ffmpeg.input(input_path)
        stream = ffmpeg.output(stream, output_av1_path, vcodec="libsvtav1", acodec="aac", **{"crf": 35, "preset": "6"})
        ffmpeg.run(stream, capture_stdout=True, capture_stderr=True, overwrite_output=True)
        conversions.append(output_av1_path)

    if not conversions:
        return JSONResponse({"ERROR": "Select at least ONE video format to convert"}, status_code=400)

    os.remove(input_path)

    if len(conversions) == 1:
        output_file = conversions[0]
        with open(output_file, "rb") as f:
            file_bytes = f.read()
        media_type = "video/webm" if output_file.endswith(".webm") else "video/mp4"
        return Response(content=file_bytes, media_type=media_type)

@app.post("/encoding_ladder")
async def encoding_ladder_endpoint(
    file: UploadFile = File(...),
    r1080p: bool = Form(...),
    r720p: bool = Form(...),
    r480p: bool = Form(...),
    r360p: bool = Form(...),
    r240p: bool = Form(...)
):
    video_bytes = await file.read()
    input_path = os.path.join(IMAGE_FOLDER, "temp_encoding_ladder_input.mp4")

    with open(input_path, "wb") as f:
        f.write(video_bytes)

    ladder_options = {
        "1080p": (1920, 1080),
        "720p": (1280, 720),
        "480p": (854, 480),
        "360p": (640, 360),
        "240p": (426, 240)
    }

    ladder = []
    if r1080p: ladder.append("1080p")
    if r720p: ladder.append("720p")
    if r480p: ladder.append("480p")
    if r360p: ladder.append("360p")
    if r240p: ladder.append("240p")

    if not ladder:
        return JSONResponse({"ERROR": "Select at least ONE ladder option"}, status_code=400)

    generated_files = []
    for resolution in ladder:
        width, height = ladder_options[resolution]
        output_path = os.path.join(RESULT_VIDEO_FOLDER, f"output_{resolution}.mp4")
        ffmpeg.input(input_path).output(output_path, vf=f"scale={width}:{height}").run(capture_stdout=True, capture_stderr=True, overwrite_output=True)
        generated_files.append(output_path)

    os.remove(input_path)  
    with open(output_path, "rb") as f:
        return Response(content=f.read(), media_type="video/mp4")