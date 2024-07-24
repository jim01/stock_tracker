FROM python:3.11-alpine3.19

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Added because it needs to compile ffi for arm64
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers && apk add libffi-dev

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/
