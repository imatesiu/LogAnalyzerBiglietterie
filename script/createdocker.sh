docker rm -f rpm-log-viewer
docker build -t rpm-log-viewer .
#docker run -d --name rpm-log-viewer  -p 8443:5000 -v "$(pwd)/tls:/app/tls:ro" -v "$(pwd)/uploads:/app/uploads" --restart unless-stopped  rpm-log-viewer
docker run -d --name rpm-log-viewer -p 8443:5000 -v "$(pwd)/etc/letsencrypt/live/rtapp.isti.cnr.it:/app/tls:ro" -v "$(pwd)/uploads:/app/uploads" --restart unless-stopped  rpm-log-viewer

