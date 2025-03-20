FROM python:3.13.2-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/app/.venv/bin:$PATH"

RUN apt-get update && \
    apt-get -y install gcc postgresql curl ca-certificates && \
    apt-get clean

COPY celery/start_worker.sh /start_worker.sh
RUN chmod +x /start_worker.sh

COPY celery/start_beat.sh /start_beat.sh
RUN chmod +x /start_beat.sh

COPY celery/start_flower.sh /start_flower.sh
RUN chmod +x /start_flower.sh

ADD . /app
WORKDIR /app

RUN uv sync --frozen --no-dev