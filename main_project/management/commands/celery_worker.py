import shlex
import subprocess
import sys
from typing import Self

from django.core.management.base import BaseCommand
from django.utils import autoreload


def restart_celery() -> None:
    """Rerstart celery."""
    celery_worker_cmd = "uv run celery -A main_project worker"
    cmd = f'pkill -f "{celery_worker_cmd}"'
    if sys.platform == "win32":
        cmd = "taskkill /f /t /im celery.exe"

    subprocess.call(shlex.split(cmd))  # noqa:S603
    subprocess.call(shlex.split(f"{celery_worker_cmd} --loglevel=info"))  # noqa:S603


class Command(BaseCommand):
    """Add django command."""

    def handle(self: Self, *args: str, **options: str) -> None:  # noqa:ARG002
        """Django handle command."""
        print("Starting celery worker with autoreload...")  # noqa:T201
        autoreload.run_with_reloader(restart_celery)
