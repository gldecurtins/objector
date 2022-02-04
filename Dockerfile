# syntax=docker/dockerfile:1
FROM python:3.10.2
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /opt
RUN apt-get update && \
    apt-get install -y gettext && \
    apt-get clean && rm -rf /var/cache/apt/* && rm -rf /var/lib/apt/lists/* && rm -rf /tmp/*
RUN pip install --upgrade pip
COPY requirements-dev.txt /opt/
RUN pip install -r requirements-dev.txt
COPY . /opt/
