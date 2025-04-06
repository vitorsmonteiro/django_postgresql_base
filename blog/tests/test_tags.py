import pytest
from django.utils.safestring import SafeText

from blog.templatetags.blog_tags import markdown_content


@pytest.mark.parametrize(
    ("input_text", "expected_output"),
    [
        ("# Heading", "<h1>Heading</h1>"),
        ("**bold text**", "<p><strong>bold text</strong></p>"),
        ("", ""),  # Test empty string
    ],
)
def test_markdown_content(input_text: str, expected_output: str) -> None:
    """Test markdown content tag."""
    result = markdown_content(input_text)
    assert isinstance(result, SafeText)
    assert result == expected_output
