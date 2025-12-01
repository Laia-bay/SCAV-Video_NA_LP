FROM python:3.10-slim

WORKDIR /app

# Install system-level dependencies ffmpeg is required for your script
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY first_seminar.py .
COPY api.py .

COPY website/streamlit_web.py .
COPY website/tabs/home_tab.py .
COPY website/tabs/images_tab.py .
COPY website/tabs/videos_tab.py .

COPY images ./images
COPY image_results ./image_results

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install fastapi uvicorn


RUN mkdir -p image_results

# since we are using FastAPI
EXPOSE 8000 
EXPOSE 8501

CMD ["bash", "-c", "uvicorn api:app --host 0.0.0.0 --port 8000 & streamlit run website/streamlit_web.py --server.port 8501"]