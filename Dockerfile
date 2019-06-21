FROM python:3.7.3-alpine3.9

RUN apk update \
    && apk add ca-certificates wget \
    && update-ca-certificates

RUN apk add --no-cache \
    postgresql-dev \
    g++ \
    gcc

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app
