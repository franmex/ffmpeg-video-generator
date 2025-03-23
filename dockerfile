FROM python:3.9-slim

# Instalar FFmpeg y dependencias
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get install -y libsndfile1 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Instalar librerías de Python
RUN pip install flask requests librosa numpy

CMD ["python", "app.py"]
