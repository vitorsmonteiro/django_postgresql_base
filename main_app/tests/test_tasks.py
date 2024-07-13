import pytest

from main_app.tasks import add, mul, xsum


@pytest.mark.parametrize(("x", "y"), [(1, 2), (3.5, 4)])
def test_add(x: float, y: float) -> None:
    """Test add()."""
    actual = add(x, y)
    assert actual == x + y


@pytest.mark.parametrize(("x", "y"), [(1, 2), (3.5, 4)])
def test_mull(x: float, y: float) -> None:
    """Test mul()."""
    actual = mul(x, y)
    assert actual == x * y


@pytest.mark.parametrize(("x"), [[1, 2], [3.5, 4]])
def test_xsum(x: list) -> None:
    """Test xsum."""
    actual = xsum(x)
    assert actual == sum(x)
