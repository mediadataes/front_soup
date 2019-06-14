FROM python:3.7-alpine

RUN apk add --no-cache \
    postgresql-dev \
    g++ \
    gcc

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app
