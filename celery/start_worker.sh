#!/bin/bash

set -o errexit
set -o nounset

uv run python manage.py celery_worker