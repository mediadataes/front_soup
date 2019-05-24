FROM python:3.7-alpine

RUN apk add --no-cache \
    postgresql-dev \
    #libc-dev \
    libxml2-dev \
    libxslt-dev \
    g++ \
    gcc
    #jpeg-dev \
    #zlib-dev \
    #libffi-dev \
    #make \
    #openssl-dev

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app
