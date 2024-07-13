from celery import shared_task  # type: ignore[attr-defined]


@shared_task
def add(x: float, y: float) -> int | float:
    """Add two number X and Y.

    Args:
        x (float): First number (X).
        y (float): Second number (y)

    Returns:
        int | float: X + Y
    """
    return x + y


@shared_task
def mul(x: float, y: float) -> int | float:
    """Multiple two number X and Y.

    Args:
        x (float): First number (X).
        y (float): Second number (y)

    Returns:
        int | float: X * Y
    """
    return x * y


@shared_task
def xsum(numbers: list[float]) -> int | float:
    """Sum all number in list numbers.

    Args:
        numbers (list[float]): List with numbers to be added.

    Returns:
        int | float: Total sum.
    """
    return sum(numbers)


@shared_task()
def say_hello() -> None:
    """Demo scheduled task."""
    print("Hello")  # noqa: T201
