"""Views for the working with routing in home application.
Contains function-based views responsible for rendering pages based on template."""
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def home_view(request: HttpRequest) -> HttpResponse:
    """View function for home page."""
    return render(request, "home/index.html",
                  {"title": "home", "data": "Welcome to the home page"})


def about_view(request: HttpRequest) -> HttpResponse:
    """View function for about page."""
    return render(request, "home/index.html",
                  {"title": "about", "data": "About page"})


def contact_view(request: HttpRequest) -> HttpResponse:
    """View function for contact page."""
    return render(request, "home/index.html",
                  {"title": "contact", "data": "Contact us"})


def post_view(request: HttpRequest, post_id: int) -> HttpResponse:
    """View function for post page."""
    return render(request, "home/index.html",
                  {"title": f"post {post_id}",
                   "data": f"You are viewing the post with ID: {post_id}"})


def profile_view(request: HttpRequest, username: str) -> HttpResponse:
    """View function for profile page."""
    return render(request, "home/index.html",
                  {"title": username,
                   "data": f"You are viewing the user profile: {username}"})


def event_view(request: HttpRequest, year: int, month: int, day: int) -> HttpResponse:
    """View function for event page."""
    return render(request, "home/index.html",
                  {"title": f"{year}/{month}/{day}",
                   "data": f"Event date: {year}-{month}-{day}"})
