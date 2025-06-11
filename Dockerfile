FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev musl-dev \
    gdal-bin libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

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
EXPOSE  9000
ENTRYPOINT ["sh", "./entrypoint.sh"]
