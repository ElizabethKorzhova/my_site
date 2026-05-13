"""This module contains WebSocket routing for realtime application."""
from typing import List

from django.urls import path, URLPattern

from .consumers import RealtimeConsumer

websocket_urlpatterns: List[URLPattern]= [
    path("ws/realtime/", RealtimeConsumer.as_asgi()),
]