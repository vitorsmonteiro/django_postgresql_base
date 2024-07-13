#!/bin/bash

set -o errexit
set -o nounset

rm -f './celerybeat.pid'
# celery -A main_project beat -l info -Q high_priority,default
celery -A main_project beat -l info
