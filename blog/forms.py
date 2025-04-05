from typing import ClassVar

from django import forms

from blog.models import BlogPost, Topic


class TopicForm(forms.ModelForm):
    """Topic form."""

    class Meta:
        """Class meta data."""

        model = Topic
        fields: ClassVar[list[str]] = ["name"]


class BlogPostForm(forms.ModelForm):
    """Post form."""

    class Meta:
        """Class meta data."""

        model = BlogPost
        fields: ClassVar[list[str]] = [
            "title",
            "topic",
            "image",
            "content",
            "previous",
        ]
