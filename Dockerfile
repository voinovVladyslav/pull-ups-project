FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

COPY . ./app
WORKDIR /app

EXPOSE 8000

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt
