FROM python:3.13.2-slim
COPY --from=ghcr.io/astral-sh/uv:0.6.8 /uv /uvx /bin/

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

RUN apt-get update && \
    apt-get -y install gcc postgresql procps && \
    apt-get clean

RUN pip install --upgrade pip
RUN pip install poetry

COPY celery/start_worker.sh /start_worker.sh
RUN chmod +x /start_worker.sh

COPY celery/start_beat.sh /start_beat.sh
RUN chmod +x /start_beat.sh

COPY celery/start_flower.sh /start_flower.sh
RUN chmod +x /start_flower.sh

ADD . /app
RUN uv sync --frozen
