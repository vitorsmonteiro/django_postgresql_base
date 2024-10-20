import shlex
import subprocess
import sys
from typing import Any, Self

from django.core.management.base import BaseCommand
from django.utils import autoreload


def restart_celery() -> None:
    """Restart celery worker."""
    celery_worker_cmd = "celery -A main_project worker"
    cmd = f'pkill -f "{celery_worker_cmd}"'
    if sys.platform == "win32":
        cmd = "taskkill /f /t /im celery.exe"

    subprocess.call(shlex.split(cmd))  # noqa: S603
    subprocess.call(shlex.split(f"{celery_worker_cmd} --loglevel=info"))  # noqa: S603


class Command(BaseCommand):
    """Commands."""

    def handle(self: Self, *args: Any, **options: Any) -> None:  # noqa: ARG002, ANN401
        """Create command to restart celery worker."""
        print("Starting celery worker with autoreload...")  # noqa: T201
        autoreload.run_with_reloader(restart_celery)
