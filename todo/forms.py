from typing import ClassVar

from django import forms

from todo.models import Task


class TaskForm(forms.ModelForm):
    """Task form."""

    title = forms.CharField(required=True)
    description = forms.TextInput()
    status = forms.ChoiceField(required=True, choices=Task.STATUS_CHOICES)

    class Meta:
        """Form meta data."""

        model = Task
        fields: ClassVar[list[str]] = ["title", "description", "status"]
