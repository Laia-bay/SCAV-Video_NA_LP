import os
import pytest
import ffmpeg
import numpy as np
from PIL import Image


def test_rgb2yuv(client):
    response = client.post("/rgb2yuv", data={"r": 255, "g": 0, "b": 0})
    assert response.status_code == 200
    data = response.json()
    assert "Y" in data and "U" in data and "V" in data

def test_yuv2rgb(client):
    response = client.post("/yuv2rgb", data={"Y": 76, "U": 84, "V": 255})
    assert response.status_code == 200
    data = response.json()
    assert "R" in data and "G" in data and "B" in data

def test_resize_image(client, test_image_path):
    with open(test_image_path, "rb") as f:
        response = client.post("/resize_image", files={"file": ("test_img.jpg", f)}, data={"width": 32, "height": 32})
    assert response.status_code == 200
    # Optionally: check if returned bytes can be opened as an image
    from io import BytesIO
    img = Image.open(BytesIO(response.content))
    assert img.size == (32, 32)

def test_serpentine(client, test_image_path):
    with open(test_image_path, "rb") as f:
        response = client.post("/serpentine", files={"file": ("test_img.jpg", f)})
    assert response.status_code == 200

def test_bw(client, test_image_path):
    with open(test_image_path, "rb") as f:
        response = client.post("/B&W", files={"file": ("test_img.jpg", f)})
    assert response.status_code == 200

def test_resize_video(client, test_video_path):
    with open(test_video_path, "rb") as f:
        response = client.post("/resize_video", files={"file": ("test_video.mp4", f)}, data={"width": 160, "height": 120})
    assert response.status_code == 200

def test_chroma_subsampling_endpoint(client, test_image_path):
    with open(test_image_path, "rb") as f:
        response = client.post("/chroma_subsampling", files={"file": f}, data={"subsampling": "420"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpg"

def test_video_info_endpoint(client, test_video_path):
    with open(test_video_path, "rb") as f:
        response = client.post("/video_info", files={"file": f})
    assert response.status_code == 200
    data = response.json()
    assert "video_codec_name" in data
    assert "audio_codec_name" in data

def test_create_BBB_container_endpoint(client, test_video_path):
    with open(test_video_path, "rb") as f:
        response = client.post(
            "/create_BBB_container",
            files={"file": f},
            data={"AAC_audio": True, "MP3_audio": False, "AC3_audio": False}
        )
    assert response.status_code == 200
    assert response.headers["content-type"] == "video/mp4"

def test_inspect_mp4_tracks_endpoint(client, test_video_path):
    with open(test_video_path, "rb") as f:
        response = client.post("/inspect_mp4_tracks", files={"file": f})
    assert response.status_code == 200
    data = response.json()
    assert "total_tracks" in data
    assert "video_tracks" in data
    assert "audio_tracks" in data

def test_macroblocks_motion_vectors_endpoint(client, test_video_path):
    with open(test_video_path, "rb") as f:
        response = client.post("/macroblocks_motion_vectors", files={"file": f})
    assert response.status_code == 200
    assert response.headers["content-type"] == "video/mp4"

def test_yuv_histogram_endpoint(client, test_video_path):
    with open(test_video_path, "rb") as f:
        response = client.post("/yuv_histogram", files={"file": f})
    assert response.status_code == 200
    assert response.headers["content-type"] == "video/mp4"

def test_convert_video_format_endpoint(client, test_video_path):
    with open(test_video_path, "rb") as f:
        response = client.post(
            "/convert_video_format",
            files={"file": f},
            data={"VP8": True, "VP9": False, "h265": False, "AV1": False}
        )
    assert response.status_code == 200
    assert response.headers["content-type"] in ["video/mp4", "video/webm"]

def test_encoding_ladder_endpoint(client, test_video_path):
    with open(test_video_path, "rb") as f:
        response = client.post(
            "/encoding_ladder",
            files={"file": f},
            data={"r1080p": False, "r720p": True, "r480p": False, "r360p": False, "r240p": False}
        )
    assert response.status_code == 200
    assert response.headers["content-type"] == "video/mp4"
