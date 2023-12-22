FROM python:3.8

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgdal-dev \
    gcc \
    python3-dev \
    python3-gdal && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .