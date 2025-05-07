FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev musl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Expose le port du serveur Django
EXPOSE  7000
ENTRYPOINT ["sh", "./entrypoint.sh"]