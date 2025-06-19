FROM python:3.12-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    python3-dev \
    gdal-bin \
    libgdal-dev \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Export des variables d'environnement nécessaires à GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Rendre le script exécutable
RUN chmod +x ./entrypoint.sh

# Expose le port du serveur Django
EXPOSE  5000
ENTRYPOINT ["sh", "./entrypoint.sh"]
