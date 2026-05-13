"""This module represents views for the working with routing in realtime application."""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def realtime_page(request: HttpRequest) -> HttpResponse:
    """Renders realtime WebSocket demo page."""
    return render(request, "realtime/realtime.html")
