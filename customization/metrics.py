"""This module contains simple server metrics."""

REQUESTS_COUNT = 0


def increment_requests_count() -> int:
    """Increases requests count and return current value."""
    global REQUESTS_COUNT
    REQUESTS_COUNT += 1

    return REQUESTS_COUNT


def get_requests_count() -> int:
    """Returns requests count."""
    return REQUESTS_COUNT
