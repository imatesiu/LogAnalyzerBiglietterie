docker build -t rpm-log-viewer .
docker run --rm -p 8443:5000 -v "$(pwd)/tls:/app/tls:ro" -v "$(pwd)/uploads:/app/uploads" --restart unless-stopped  rpm-log-viewer

