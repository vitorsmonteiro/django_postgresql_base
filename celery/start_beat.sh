#!/bin/bash

set -o errexit
set -o nounset

rm -f './celerybeat.pid'
uv run celery -A main_project beat -l info
