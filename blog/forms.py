from typing import ClassVar

from django import forms

from blog.models import Topic


class TopicForm(forms.ModelForm):
    """Topic form."""

    class Meta:
        """Class meta data."""

        model = Topic
        fields: ClassVar[list[str]] = ["name"]
