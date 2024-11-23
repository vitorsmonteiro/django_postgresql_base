FROM python:3.11.4-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get -y install gcc postgresql && \
    apt-get clean

RUN pip install --upgrade pip
RUN pip install poetry

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --without dev

COPY celery/start_worker.sh /start_worker.sh
RUN chmod +x /start_worker.sh

COPY celery/start_beat.sh /start_beat.sh
RUN chmod +x /start_beat.sh

COPY celery/start_flower.sh /start_flower.sh
RUN chmod +x /start_flower.sh

COPY . .