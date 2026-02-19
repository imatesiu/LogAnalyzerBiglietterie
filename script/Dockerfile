FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# (Opzionale) utile se devi verificare certificati di sistema, ecc.
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia codice
COPY . /app

# Crea upload dir (se non già presente)
RUN mkdir -p /app/uploads

EXPOSE 5000

# HTTPS direttamente da gunicorn usando tls/fullchain.pem e tls/key.pem
CMD ["gunicorn", "-b", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "--timeout", "120", "app:app", "--certfile", "/app/tls/fullchain.pem", "--keyfile", "/app/tls/key.pem"]

