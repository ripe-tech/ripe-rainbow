FROM debian:latest

LABEL version="1.0"
LABEL maintainer="Platforme <development@platforme.com>"

ENV LEVEL DEBUG
ENV VNC_RESOLUTION "${VNC_RESOLUTION:-1920x1080x32}"

ENV DRIVER selenium
ENV SEL_HEADLESS 0
ENV SEL_BROWSER chrome
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

RUN apt-get update \
  && apt-get install -y git curl unzip jq python3 python3-pip python3-setuptools \
  && curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_$(dpkg --print-architecture).deb -o /tmp/chrome.deb \
  && apt-get install -y /tmp/chrome.deb \
  && export CHROMEDRIVER_VERSION=$(google-chrome --version | cut -d ' ' -f 3 | cut -d '.' -f 1) \
  && curl -sSL https://chromedriver.storage.googleapis.com/$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEDRIVER_VERSION)/chromedriver_linux64.zip -o /tmp/chromedriver_linux64.zip \
  && unzip /tmp/chromedriver_linux64.zip -d /usr/bin

RUN apt-get update \
  && curl -sSL "https://download.mozilla.org/?product=firefox-devedition-latest-ssl&os=linux64" -o /tmp/firefox.tar.bz2 \
  && apt-get install -y libdbus-glib-1-2 libgtk2.0-0 \
  && tar xjfv /tmp/firefox.tar.bz2 -C /opt/ \
  && ln -s /opt/firefox/firefox /usr/bin/firefox \
  && export GECKODRIVER_VERSION=$(curl -sL https://api.github.com/repos/mozilla/geckodriver/releases/latest | jq -r .name) \
  && curl -sSL https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz -o /tmp/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz \
  && tar zxvf /tmp/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/bin
