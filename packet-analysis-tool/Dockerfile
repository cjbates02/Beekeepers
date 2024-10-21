
FROM ubuntu:latest


RUN apt-get update && apt-get install -y \
    tcpdump \
    socat \
    && rm -rf /var/lib/apt/lists/*


CMD ["sh", "-c", "tcpdump -i any -U -w - | socat - TCP-LISTEN:12345,fork"]