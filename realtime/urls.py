"""URL configuration for realtime application in my_site project.
The `urlpatterns` list routes URLs to corresponding views."""
from typing import List

from django.urls import path, URLPattern

from .views import realtime_page

urlpatterns: List[URLPattern] = [
    path("", realtime_page, name="realtime"),
]