FROM ubuntu:latest
LABEL authors="kgrum"

ENTRYPOINT ["top", "-b"]