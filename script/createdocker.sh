docker build -t rpm-log-viewer .
#docker run  -p 8443:5000 -v "$(pwd)/tls:/app/tls:ro" -v "$(pwd)/uploads:/app/uploads" --restart unless-stopped  rpm-log-viewer
docker run  -p 8443:5000 -v "$(pwd)/tls:/etc/letsencrypt/live/rtapp.isti.cnr.it:ro" -v "$(pwd)/uploads:/app/uploads" --restart unless-stopped  rpm-log-viewer

