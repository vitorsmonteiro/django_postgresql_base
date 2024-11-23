from typing import ClassVar

from django.forms import ModelForm

from main_app.models import Car, Manufacturer


class CarForm(ModelForm):
    """Car basic form."""

    model = Car
    fields: ClassVar[list[str]] = ["name", "manufacturer"]


class ManufacturerForm(ModelForm):
    """Manufacturer basic form."""

    model = Manufacturer
    fields: ClassVar[list[str]] = ["name"]
