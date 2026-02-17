"""URL configuration for main application in my_site project.
The `urlpatterns` list routes URLs to corresponding views."""

from django.urls import path, URLPattern
from . import views

urlpatterns: list[URLPattern] = [
    path("home/", views.home_view, name="main_home"),
    path("about/", views.about_view, name="main_about"),
    path("contacts/", views.ContactView.as_view(), name="main_contact"),
    path("services/", views.ServiceView.as_view(), name="main_services"),
]
