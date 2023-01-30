FROM hivesolutions/python:latest

LABEL version="1.0"
LABEL maintainer="Platforme <development@platforme.com>"

ENV DRIVER selenium
ENV SEL_HEADLESS 1
ENV SEL_BROWSER chrome

RUN echo "http://dl-4.alpinelinux.org/alpine/v3.4/main" >> /etc/apk/repositories
RUN	echo "http://dl-4.alpinelinux.org/alpine/v3.4/community" >> /etc/apk/repositories
RUN apk update && apk add chromium chromium-chromedriver
