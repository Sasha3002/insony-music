# Używamy oficjalnego obrazu Python 3.11
FROM python:3.11-slim

# Ustawiamy zmienne środowiskowe
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Ustawiamy katalog roboczy
WORKDIR /app

# Instalujemy zależności systemowe
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Kopiujemy requirements.txt i instalujemy zależności Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Kopiujemy cały kod projektu
COPY . .

# Tworzymy katalogi dla media i static files
RUN mkdir -p /app/media /app/staticfiles

# Otwieramy port 8000
EXPOSE 8000

# Domyślna komenda
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]