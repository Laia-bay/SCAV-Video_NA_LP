FROM python:3.10-slim

WORKDIR /app

# Install system-level dependencies ffmpeg is required for your script
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY first_seminar.py .
COPY app.py .
COPY images ./images
COPY image_results ./image_results

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir -p image_results

# since we are using streamlit...
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]