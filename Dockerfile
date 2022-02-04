# syntax=docker/dockerfile:1
FROM python:3.10.2

WORKDIR /app

ARG REQUIREMENTS=requirements-dev.txt
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y gettext && \
    apt-get clean && rm -rf /var/cache/apt/* && rm -rf /var/lib/apt/lists/* && rm -rf /tmp/*

COPY requirements.txt requirements-dev.txt /app/
RUN pip install --upgrade --no-cache-dir --requirement $REQUIREMENTS --disable-pip-version-check

COPY . /app/
