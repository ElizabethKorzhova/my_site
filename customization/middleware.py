"""This module contains custom middleware for customization app."""
from collections.abc import Callable

from django.http import HttpRequest, HttpResponse

from .metrics import increment_requests_count


class CustomHeaderMiddleware:
    """Middleware that adds custom header to every response."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Initializes middleware."""
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Adds custom header to response."""
        response = self.get_response(request)
        response["X-Custom-Header"] = "Customization App"

        return response


class RequestMetricsMiddleware:
    """Middleware that counts server requests."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Initializes middleware."""
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Counts request and add metric header to response."""
        requests_count = increment_requests_count()

        response = self.get_response(request)
        response["X-Requests-Count"] = str(requests_count)

        return response
