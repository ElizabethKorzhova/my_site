"""Views for main application in my_site project to render templates.
Contains function-based and class-based views responsible for rendering pages based on templates."""
import datetime

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View

from .data import DATA
from .types import ServiceType


def home_view(request: HttpRequest) -> HttpResponse:
    """View function for home page in main app of my_site project."""
    return render(request, "main/home.html",
                  {"company_name": DATA["company_name"], "greeting_text": DATA["greeting_text"], })


def about_view(request: HttpRequest) -> HttpResponse:
    """View function for home page in main app of my_site project."""
    return render(request, "main/about.html",
                  {"company_description": DATA["company_description"]})


class ContactView(View):
    """View class for contact page in main app of my_site project."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Method to render contact page in main app of my_site project."""
        context_contacts: dict[str, str] = {
            "address": DATA["address"],
            "phone": DATA["phone"],
            "email": DATA["email"]
        }
        return render(request, "main/contact.html", context_contacts)


class ServiceView(View):
    """View class for service page in main app of my_site project."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Method to render service page in main app of my_site project."""
        query: str | None = request.GET.get("q")
        services: list[ServiceType] = DATA["services"]

        all_services_count = len(services)
        no_services = False
        search_performed = False

        if not services:
            no_services = True

        elif query:
            search_performed = True
            services = [
                service for service in services if
                query.lower() in service["service_title"].lower() or query.lower() in service[
                    "service_description"].lower()
            ]

        if not search_performed:
            services = services if request.GET.get("show") == "all" else services[:3]

        context_services: dict[str, list[dict[str, str]] | datetime.datetime | bool] = {
            "services": services,
            "all_services_count": all_services_count,
            "date": datetime.datetime.now(),
            "no_services": no_services,
            "search_performed": search_performed
        }

        return render(request, "main/services.html", context_services)
