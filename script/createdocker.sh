#!/usr/bin/env bash
set -euo pipefail

# Avvio stack produzione:
# - viewer (gunicorn HTTP interno)
# - reverse-proxy (nginx con TLS su 8443)
# Pulisce eventuale container legacy avviato con docker run.
docker rm -f rpm-log-viewer >/dev/null 2>&1 || true

# Ricrea stack compose da zero.
docker compose down --remove-orphans
docker compose up -d --build --force-recreate

echo "Stack avviata: https://<host>:8443"
