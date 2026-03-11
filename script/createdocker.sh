#!/usr/bin/env bash
set -euo pipefail

# Avvio stack produzione:
# - viewer (gunicorn HTTP interno)
# - reverse-proxy (nginx con TLS su 8443)
docker compose down
docker compose up -d --build

echo "Stack avviata: https://<host>:8443"
