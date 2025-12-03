# SCAV-Video_NA_LP
This repository is done for the subject Sistemes de Codificació d'Àudio i Video.  Especially for the Video Part. This is property of Nahia and Laia. 

This is based on 2 different things:
    - A jupyter notebook called: first_seminar.ipynb, where the first seminar has been done. It has 2 parts, the whole coding of functions, and the testing of said functions.
    - A docker that works with both FastAPI and Streamlit.
    FastAPI works as backend whereas Streamlit as frontend. 
    Streamlit is the "aesthetic" website that we have customized to make it look good and user-friendly. On the website you can select or upload images and do several processing operations to them. These operations will be done because Streamlit will call the API, and return the resulting image. (If it is a video, it will return only an "OK" message)

To build the docker you must write on CMD: docker-compose build seminar01 .
Then, to run it, you must write: docker-compose up
    - FastAPI will be accessed through: http://localhost:8000/docs
    - Streamlit will be accessed through: http://localhost:8501


In the images folder you will find several example of images that you can use for the different endpoints, or for the first seminar notebook. The resulting images will be saved on the "image_results" folder.
    - For the first part of first_seminar.ipynb, resulting images will have the name "example_{operation_done}.jpg", and they are done with "ref.jpg".
    - For the second part of first_seminar.ipynb, that is, the tests, images will be saved as "test_{operation_done}.jpg". In this part you can choose any image you want from the folder.
    - For the API and the Streamlit website, images will be saved as "output_{operation_done}.jpg. In these 2 cases, you can choose an image from the images folder, or an image of your own computer (as long as it is .jpg).

For the videos, we have mostly used the Big Buck Bunny, however for the video conversions we used other videos that were shorter in duration. You can find some videos examples on this Google Drive folder:
https://drive.google.com/drive/folders/1bUrzpWsFjtYViLBdtIchkHKftN0V5jxC?usp=sharing

    - For the API and the Streamlit website, videos will be saved as "output_{operation_done}.mp4" (or .webm) on the video_results folder. And again, you can choose one of the videos of the google drive folder, or one of your own.

