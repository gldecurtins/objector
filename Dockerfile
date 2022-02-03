# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /django
COPY requirements-dev.txt /django/
RUN pip install --upgrade pip
RUN pip install -r requirements-dev.txt
COPY . /django/
