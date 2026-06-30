FROM python:3.11-slim

WORKDIR /app

# Dépendances système pour TensorFlow et OpenCV
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-dri \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Créer les dossiers nécessaires pour la persistance
RUN mkdir -p /app/uploads/diagnostics /app/models

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
