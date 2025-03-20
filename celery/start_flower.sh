#!/bin/bash

set -o errexit
set -o nounset

worker_ready() {
    uv run celery -A main_project inspect ping
}

until worker_ready; do
  >&2 echo 'Celery workers not available'
  sleep 1
done
>&2 echo 'Celery workers is available'

uv run celery -A main_project  \
    --broker="${CELERY_BROKER}" \
    flower