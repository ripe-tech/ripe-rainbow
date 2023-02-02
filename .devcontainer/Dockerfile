FROM debian:latest

LABEL version="1.0"
LABEL maintainer="Platforme <development@platforme.com>"

ENV DRIVER selenium
ENV SEL_HEADLESS 0
ENV SEL_BROWSER chrome

RUN apt-get update && apt-get install -y chromium chromium-driver
