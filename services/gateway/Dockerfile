# syntax=docker/dockerfile:1.7

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY ../shared/requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /tmp/requirements.txt

COPY ./gateway/ /app/

ENV APP_MODULE=app.main:app \
    APP_PORT=2323

EXPOSE 2323

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "2323", "--reload"]
