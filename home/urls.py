"""URL configuration for home application in my_site project.
The `urlpatterns` list routes URLs to corresponding views."""

from django.urls import path, re_path, URLPattern
from . import views

urlpatterns: list[URLPattern] = [
    path("home/", views.home_view, name="home"),
    path("about/", views.about_view, name="about"),
    path("contact/", views.contact_view, name="contact"),
    re_path(r"^post/(?P<post_id>\d+)/$", views.post_view, name="post"),
    re_path(r"^profile/(?P<username>[A-za-z]+)/$", views.profile_view, name="profile"),
    re_path(r"^event/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$", views.event_view,
            name="event"),
]
