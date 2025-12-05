FROM python:3.10-slim

WORKDIR /app

# Install system-level dependencies ffmpeg is required for your script
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
    

COPY requirements.txt .
COPY fastapi_files/first_seminar.py .
COPY fastapi_files/api.py .

COPY website/streamlit_web.py .
COPY website/tabs/home_tab.py .
COPY website/tabs/images_tab.py .
COPY website/tabs/videos_tab.py .

COPY tests/test_first_seminar.py .
COPY tests/test_api.py .
COPY tests/conftest.py .

COPY images ./images
COPY image_results ./image_results
COPY video_results ./video_results

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install pytest


RUN mkdir -p image_results
RUN mkdir -p video_results

# since we are using FastAPI
EXPOSE 8000 
EXPOSE 8501

CMD ["bash", "-c", "uvicorn fastapi_files.api:app --host 0.0.0.0 --port 8000 & streamlit run website/streamlit_web.py --server.port 8501"]