"""Views for the working with routing in board application.
Contains function-based views responsible for rendering pages based on template."""
from datetime import timedelta

from django.db.models import Count
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import CustomUser, Ad, Category


def board_view(request: HttpRequest) -> HttpResponse:
    """View function for board page."""
    categories = Category.objects.all()
    ads = Ad.objects.annotate(comments_count=Count("comments"))

    category_id = request.GET.get("category")
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        ads = ads.filter(category=category, is_active=True)

    if request.GET.get("active"):
        ads = ads.filter(is_active=True)

    if request.GET.get("recent"):
        last_month = timezone.now() - timedelta(days=30)
        ads = ads.filter(created_at__gte=last_month)

    return render(request, "board/board.html",
                  {"categories": categories, "ads": ads,
                   "ads_count": ads.count()})


def user_view(request: HttpRequest, user_id: int) -> HttpResponse:
    """View function for user page."""
    user = get_object_or_404(CustomUser, id=user_id)

    ads = user.ads.annotate(comments_count=Count("comments"))

    return render(request, "board/user.html",
                  {"user": user, "ads": ads})


def ad_view(request: HttpRequest, ad_id: int) -> HttpResponse:
    """View function for ad page."""
    ad = get_object_or_404(Ad, id=ad_id)

    ad.deactivate()
    comments = ad.comments.all()

    return render(request, "board/ad.html",
                  {"ad": ad, "comments": comments})
