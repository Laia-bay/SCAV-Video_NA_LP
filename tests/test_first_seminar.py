from fastapi_files.first_seminar import colors, resizing, serpentine_pattern, black_white, DCT, DWT
from PIL import Image
import numpy as np
import os


def test_rgb2yuv_and_back():
    rgb = [100, 150, 200]
    yuv = colors.rgb2yuv(rgb)
    rgb_back = colors.yuv2rgb(yuv)

    # Allow small numerical differences
    for a, b in zip(rgb, rgb_back):
        assert abs(a - b) < 5


def test_resize_image(tmp_path, test_image_path):
    output_path = tmp_path / "resized.jpg"
    output_str = resizing.resize_image(test_image_path, str(output_path), 32, 32)
    assert os.path.exists(output_str)


def test_serpentine_pattern(tmp_path, test_image_path):
    output_path = tmp_path / "serp.jpg"
    serpentine_pattern.serpentine(test_image_path, str(output_path))
    assert os.path.exists(output_path)

    out_img = Image.open(output_path)
    assert out_img.size == Image.open(test_image_path).size


def test_black_white(tmp_path, test_image_path):
    output_path = tmp_path / "bw.jpg"
    black_white.grayscale_image(test_image_path, str(output_path))
    assert os.path.exists(output_path)


def test_dct_idct_roundtrip(test_image_path):
    dct_values = DCT.dct_conversion(test_image_path, serpentine=True, bw=True)
    restored = DCT.idct_conversion(dct_values)

    assert isinstance(restored, np.ndarray)
    assert restored.shape == dct_values.shape


def test_dwt_idwt_roundtrip(test_image_path):
    dwt_values = DWT.dwt_conversion(test_image_path, True, True)
    restored = DWT.idwt_conversion(dwt_values)

    assert isinstance(restored, np.ndarray)