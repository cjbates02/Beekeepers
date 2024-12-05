
FROM ubuntu:latest


RUN apt-get update && apt-get install -y \
    tcpdump \
    socat \
    && rm -rf /var/lib/apt/lists/*


EXPOSE 8888

#CMD ["sh", "-c", "socat - TCP-LISTEN:8888,fork"]
CMD ["sh", "-c", "tcpdump -i any -U -w - | socat - TCP-LISTEN:8888,fork"]