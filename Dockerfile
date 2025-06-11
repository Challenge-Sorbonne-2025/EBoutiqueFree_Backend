FROM python:3.12-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev musl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Rendre le script exécutable (sur Linux)
RUN chmod +x ./entrypoint.sh

# Port exposé (optionnel en docker-compose)
EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]


#ENTRYPOINT ["sh", "./entrypoint.sh"]

