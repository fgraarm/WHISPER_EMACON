# Usar una imagen base oficial de Python
FROM python:3.8-slim

# Actualizar el sistema y instalar dependencias necesarias
# Asegúrate de incluir git para poder clonar repositorios
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libsndfile1 \
        portaudio19-dev \
        ffmpeg \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de la aplicación al directorio de trabajo del contenedor
COPY backend/ /app/backend
COPY frontend/ /app/frontend

# Instalar PyTorch, Flask, Transformers, SentencePiece, Sacremoses, y las dependencias necesarias
# Incluir la instalación y actualización de Whisper directamente desde GitHub
RUN pip install --no-cache-dir \
    torch \
    flask \
    transformers \
    sounddevice \
    soundfile \
    sentencepiece \
    sacremoses \
    git+https://github.com/openai/whisper.git && \
    pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git

# Exponer el puerto en el que tu aplicación se ejecutará dentro del contenedor
EXPOSE 5000

# Ajustar el comando para ejecutar app.py desde la ubicación correcta
CMD ["python", "./backend/app.py"]

