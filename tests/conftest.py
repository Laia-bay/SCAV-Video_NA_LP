import pytest
import ffmpeg
from PIL import Image
import numpy as np
import os
import uuid
from fastapi.testclient import TestClient
from fastapi_files.api import app

@pytest.fixture
def test_image_path(tmp_path):
    """Create a tiny RGB test image (64x64)."""
    img = Image.fromarray(np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8))
    path = tmp_path / f"test_image_{uuid.uuid4()}.jpg"
    img.save(path)
    return str(path)

@pytest.fixture
def test_video_path(tmp_path):
    """Create a tiny 1-second 128x72 test video using ffmpeg."""
    path = tmp_path / f"test_video_{uuid.uuid4()}.mp4"
    (
        ffmpeg
        .input("color=c=red:s=128x72:d=1", f="lavfi")
        .output(str(path), vcodec="libx264", pix_fmt="yuv420p")
        .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
    )
    return str(path)

@pytest.fixture
def client():
    """
    Provides a TestClient for the FastAPI app.
    """
    return TestClient(app)