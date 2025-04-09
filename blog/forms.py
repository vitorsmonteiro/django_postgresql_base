from typing import ClassVar

from django import forms

from blog.models import BlogPost, Topic


class TopicForm(forms.ModelForm):
    """Topic form."""

    parent_topic = forms.ModelChoiceField(queryset=Topic.objects.all(), required=False)

    class Meta:
        """Class meta data."""

        model = Topic
        fields: ClassVar[list[str]] = ["name", "parent_topic"]


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
