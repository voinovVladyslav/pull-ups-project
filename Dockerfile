FROM python:3.11.2-alpine

ENV PYTHONUNBUFFERED=1

COPY . ./app
WORKDIR /app

EXPOSE 8000

RUN python -m pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client  && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev zlib zlib-dev && \
    pip install -r requirements.txt && \
    apk del .tmp-build-deps
