import shutil
from collections.abc import Generator
from pathlib import Path

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from authentication.models import User
from main_project.settings import MEDIA_ROOT

pytestmark = pytest.mark.django_db

FIRST_NAME = "foo"
LAST_NAME = "bar"
USER_EMAIL = "foo@bar.com"
USER_PASSWORD = "password"  # noqa: S105
TOKEN = "foo"  # noqa: S105


@pytest.fixture
def user_fixture() -> User:
    """User fixture."""
    user = User(
        first_name=FIRST_NAME, last_name=LAST_NAME, email=USER_EMAIL, token=TOKEN
    )
    user.set_password(USER_PASSWORD)
    user.save()
    return user


@pytest.fixture
def user_fixture2() -> User:
    """User fixture 2."""
    user = User(first_name="foo", last_name="bar", email="foobar@mail.com", token="bar")  # noqa: S106
    user.set_password(USER_PASSWORD)
    user.save()
    return user


@pytest.fixture
def image_upload_fixture() -> Generator[SimpleUploadedFile]:
    """Image upload fixture."""
    path = Path().cwd()
    path = (
        path
        / "authentication"
        / "static"
        / "authentication"
        / "img"
        / "blank_profile.jpg"
    )
    with path.open("rb") as file:
        image = SimpleUploadedFile("image.jpg", file.read(), content_type="image/jpeg")
    yield image
    path = Path(MEDIA_ROOT)
    if path.exists and path.is_dir:
        shutil.rmtree(path=path)
