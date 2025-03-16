from typing import ClassVar

from django import forms

from blog.models import Post, Topic


class TopicForm(forms.ModelForm):
    """Topic form."""

    class Meta:
        """Class meta data."""

        model = Topic
        fields: ClassVar[list[str]] = ["name"]


class PostForm(forms.ModelForm):
    """Post form."""

    class Meta:
        """Class meta data."""

        model = Post
        fields: ClassVar[list[str]] = [
            "title",
            "topic",
            "image",
            "content",
            "previous",
        ]
