FROM python:3.6.4-stretch

RUN apt-get update -y && \
    apt-get install -y --force-yes curl && \
    curl -sL https://deb.nodesource.com/setup_9.x | bash - && \
    apt-get install -y --force-yes \
    build-essential \
    nodejs \
    npm \
    python3-pip
RUN mkdir -p /myapp
ADD . /myapp
WORKDIR /myapp
RUN npm install
ENV PATH /myapp/node_modules/.bin/:$PATH
CMD bash
