from PIL import Image as Img
import ffmpeg
import numpy as np
from scipy.fftpack import dct, idct
import pywt
import os
os.makedirs("image_results", exist_ok=True)

class colors:
    def rgb2yuv(color):
        r = color[0]
        g = color[1]
        b = color[2]

        Y = 0.257*r +0.504*g +0.098*b +16
        U = -0.148*r -0.291*g +0.439*b +128
        V = 0.439*r -0.368*g -0.071*b +128

        color_yuv = [Y, U, V]
        return color_yuv

    def yuv2rgb(color):
        Y = color[0]
        U = color[1]
        V = color[2]

        r = 1.164*(Y-16)+1.596*(V-128)
        g = 1.164*(Y-16) - 0.813*(V-128)-0.391*(U-128)
        b = 1.164*(Y-16)+2.018*(U-128)

        color_rgb = [r, g, b]
        return color_rgb
    
class resizing:
    def resize_image(input_file, output_file, width, height):

        image = Img.open(input_file)

        width_input, height_input = image.size
        print(f"The image resolution is: {width_input}x{height_input}")

        try:
            ffmpeg.input(input_file).output(output_file, vf=f"scale={width}:{height}").run(capture_stdout=True, capture_stderr=True, overwrite_output=True)
            
            print(f"Successfully resized {input_file} to {width}x{height}")
        except ffmpeg.Error as e:
            print(f"An error occurred: {e}")

        return output_file
    

class serpentine_pattern:
    
    def serpentine(input_file, output_file):
        serpentine_order = [(0,0), (1,0), (0,1), (0,2), (1,1), (2,0), (3,0), (2,1), (1,2), (0,3), (0,4), (1,3), (2,2), (3,1), (4,0), (5,0), (4,1), (3,2), (2,3), (1,4), (0,5),
                    (0,6), (1,5), (2,4), (3,3), (4,2), (5,1), (6,0), (7,0), (6,1), (5,2), (4,3), (3,4), (2,5), (1,6), (0,7), (1,7), (2,6), (3,5), (4,4), (5,3), (6,2),
                    (7,1), (7,2), (6,3), (5,4), (4,5), (3,6), (2,7), (3,7), (4,6), (5,5), (6,4), (7,3), (7,4), (6,5), (5,6), (4,7), (5,7), (6,6), (7,5), (7,6), (6,7),
                    (7,7)]
        
        image = Img.open(input_file).convert("RGB") ## convert part to get pixels in rgb value
        width, height = image.size

        pixels_im = image.load()

        pixels_read = []

        for w in range (0, width, 8):                ## start, stop, step
            for h in range (0, height, 8):

                for (x,y) in serpentine_order:           ## for each pixel (each pair of x,y coordinates)
                    pixel_x = w + x                        ## the coordinate of the serpentine plus the block that it is in
                    pixel_y = h + y
                    if pixel_x < width and pixel_y < height:
                        pixels_read.append(pixels_im[pixel_x, pixel_y])

          ## Saving list of pixels into an image
        #create array with list, and reshape into width and height of image
        array_serpentine = np.array(pixels_read, dtype=np.uint8)
        array_serpentine = array_serpentine.reshape(height, width, 3)

        # create image with array
        serpentine_image = Img.fromarray(array_serpentine)

        # save image
        serpentine_image.save(output_file)
        return output_file

class black_white:
    def grayscale_image(input_file, output_file):

        try:
            ffmpeg.input(input_file).output(output_file, vf="format = gray").run(capture_stdout=True, capture_stderr=True, overwrite_output=True)
            print(f"Successfully converted into Black & White!")
        except ffmpeg.Error as e:
            print(f"An error occurred: {e}")

        return output_file
    
class RLE:
    def run_length_encoding(datastream):
        c = 0
        count = 0

        for x in range (len(datastream)):
            if datastream[c] == '0':
                count=count+1

            if datastream[c + 1] != '0':
                print("0"+ str(count), end='')
            else:
                print(datastream[c], end='')
            c = c+1

class DCT:
    def dct_conversion (input_file,serpentine_implemented, bw_implemented):
        if serpentine_implemented == False:
            serpentine_im = serpentine_pattern.serpentine(input_file, "image_results/example_serpentine.jpg")
            input_file = serpentine_im

        if bw_implemented == False:
            grayscale_im = black_white.grayscale_image(input_file, 'image_results/example_bw_image.jpg')
            input_file = grayscale_im
        
        im = Img.open(input_file)
        result_im = np.asarray(im)
        dct_values = dct(result_im, type=2, n=None, axis=-1)

        return dct_values
    
    def idct_conversion (dct_values):
        idct_values = idct(dct_values, type=2, norm='ortho', axis=-1, overwrite_x=False)

        return idct_values
    
class DWT:
    def dwt_conversion (input_file, serpentine_implemented, bw_implemented):
        if serpentine_implemented == False:
            serpentine_im = serpentine_pattern.serpentine(input_file, "image_results/example_serpentine.jpg")
            input_file = serpentine_im

        if bw_implemented == False:
            grayscale_im = black_white.grayscale_image(input_file, 'image_results/example_bw_image.jpg')
            input_file = grayscale_im

        im = Img.open(input_file)
        im_array = np.asarray(im)
        dwt_values = pywt.dwt2(im_array, 'haar')

        return dwt_values
    
    def idwt_conversion (dwt_values):
        idwt_values = pywt.idwt2(dwt_values, 'haar')

        return idwt_values
