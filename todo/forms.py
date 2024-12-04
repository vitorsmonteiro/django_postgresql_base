from typing import ClassVar

from django import forms

from todo.models import Task, TaskCategory, TaskStatus


class TaskStatusForm(forms.ModelForm):
    """TaskStatus form."""

    name = forms.CharField(required=True)

    class Meta:
        """Form meta data."""

        model = TaskStatus
        fields: ClassVar[list[str]] = ["name"]


class TaskCategoryForm(forms.ModelForm):
    """TaskCategory form."""

    name = forms.CharField(required=True)

    class Meta:
        """Form meta data."""

        model = TaskCategory
        fields: ClassVar[list[str]] = ["name"]


class TaskForm(forms.ModelForm):
    """Task form."""

    title = forms.CharField(required=True)
    description = forms.TextInput()
    status = forms.ChoiceField(choices=TaskStatus.objects.all())
    category = forms.ChoiceField(choices=TaskCategory.objects.all())

    class Meta:
        """Form meta data."""

        model = Task
        fields: ClassVar[list[str]] = ["title", "description", "status", "category"]
