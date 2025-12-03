# SCAV-Video_NA_LP

This repository is made for the subject **Sistemes de Codificació d'Àudio i Video**, specifically for the Video part.  
This work is property of **Nahia and Laia**.

---

## Overview

This project is based on two main components:

1. **A Jupyter Notebook:**  
   - `first_seminar.ipynb`, where the first seminar has been completed.  
   - It includes two parts:  
     - The implementation of the required functions.  
     - The testing of those functions.

2. **A Docker environment with FastAPI and Streamlit:**  
   - **FastAPI** acts as the backend.  
   - **Streamlit** acts as the frontend.  
   - Streamlit provides an easy-to-use website where users can upload or select images and videos and apply several processing operations.  
   - Streamlit calls the FastAPI backend to perform the selected operation and returns the result.  
   - For video operations, Streamlit will only display an `"Video saved"` message instead of returning a processed video.

---

## How to Build and Run the Docker

To build the Docker container, run:

```cmd
docker-compose build seminar01
```
---

## Running the services

To start the services, run:

```cmd
docker-compose up
```

You can then access:

- **FastAPI**: http://localhost:8000/docs

- **Streamlit** interface: http://localhost:8501

---

## Images

Inside the images folder, you will find several example images that can be used for the API, Streamlit, or the seminar notebook.
The resulting processed images will be stored inside the image_results folder.

1. **First part** of first_seminar.ipynb:
- Resulting images follow the naming format: *example_{operation_done}.jpg*
- The reference image used is ref.jpg.

2. **Second part** of first_seminar.ipynb (testing):
- Resulting images follow the naming format: *test_{operation_done}.jpg*
- Any image from the folder can be used.

3. **API** and **Streamlit**:
- Resulting images follow the naming format: *output_{operation_done}.jpg*
- You can select an image from the images folder on streamlit, upload an image from that folder, or upload your own .jpg image.

---

## Videos

For most video operations, the **Big Buck Bunny (BBB)** video was used.
For video conversions, shorter videos were preferred, since it took too long.
Example videos can be found in the following Google Drive folder:

https://drive.google.com/drive/folders/1bUrzpWsFjtYViLBdtIchkHKftN0V5jxC?usp=sharing

API and Streamlit outputs:

Resulting videos follow the naming format: *output_{operation_done}.mp4* or *output_{operation_done}.webm*

Videos are stored in the video_results folder.

You can use the Google Drive videos or upload one of your own.

---

## Authors notes
That is all, we hope you like this project.

Sincerely, 

Nahia and Laia.