"""This module defines URL patterns for session app."""
from typing import List

from django.urls import path, URLPattern, URLResolver

from . import views

app_name = "session"

urlpatterns: List[URLPattern | URLResolver]  = [
    path("login/", views.user_login_view, name="login"),
    path("greeting/", views.greeting_view, name="greeting"),
    path("logout/", views.logout_view, name="logout"),

    path("books/unoptimized/", views.unoptimized_books_view, name="books_unoptimized"),
    path("books/optimized/", views.optimized_books_view, name="books_optimized"),
    path("books/cached/", views.cached_books_view, name="books_cached"),

    path("statistics/", views.statistics_view, name="statistics"),
    path("raw-sql/", views.raw_sql_view, name="raw_sql"),
    path("tasks/<str:task_id>/", views.task_status_view, name="task_status"),
]
