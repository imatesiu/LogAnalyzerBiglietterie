FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# openssl per p7m, ca-certificates per TLS, (lxml usa wheel -> ok)
RUN apt-get update && apt-get install -y --no-install-recommends \
      openssl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
RUN mkdir -p /app/uploads

EXPOSE 5000

# HTTPS diretto con gunicorn (cert/key montati in /app/tls)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "--timeout", "120", "app:app", "--certfile", "/app/tls/fullchain.pem", "--keyfile", "/app/tls/key.pem"]
