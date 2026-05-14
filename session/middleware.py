"""This module contains custom middleware for session app."""
from typing import Callable

from django.core.cache import cache
from django.http import HttpRequest, HttpResponse


class AnonymousBookListCacheMiddleware:
    """Middleware for caching books list page for anonymous users."""

    def __init__(self, get_response: Callable) -> None:
        """Initializes the middleware."""
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Caches response for anonymous users."""
        if (
            request.path == "/session/books/cached/"
            and not request.user.is_authenticated
            and request.method == "GET"
        ):
            cache_key = "anonymous_book_list_page"
            cached_response = cache.get(cache_key)

            if cached_response:
                return cached_response

            response = self.get_response(request)
            cache.set(cache_key, response, timeout=60 * 5)
            return response
        return self.get_response(request)
