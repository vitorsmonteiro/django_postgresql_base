FROM python:3.13.2

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Place executables in the environment at the front of the path
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
ENV UV_PROJECT_ENVIRONMENT=/usr/local

# Compile bytecode
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
ENV UV_COMPILE_BYTECODE=1

# uv Cache
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
ENV UV_LINK_MODE=copy

COPY celery/start_worker.sh /start_worker.sh
RUN chmod +x /start_worker.sh

COPY celery/start_beat.sh /start_beat.sh
RUN chmod +x /start_beat.sh

COPY celery/start_flower.sh /start_flower.sh
RUN chmod +x /start_flower.sh

ADD . /app

# Sync the project
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN uv sync --frozen --no-dev

ENTRYPOINT []
