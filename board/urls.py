"""URL configuration for board application in my_site project.
The `urlpatterns` list routes URLs to corresponding views."""
from typing import List

from django.urls import path, URLPattern

from . import views

urlpatterns: List[URLPattern] = [
    path("", views.board_view, name="board"),
    path("ad/<int:ad_id>/", views.ad_view, name="ad"),
    path("user/<int:user_id>/", views.user_view, name="user"),
]
