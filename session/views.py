"""This module contains views for customization app."""
import time

from celery.result import AsyncResult
from django.contrib import messages
from django.core.cache import cache
from django.db import connection
from django.db.models import Avg, Count
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import LoginForm
from .models import Author, BookData


COOKIE_MAX_AGE = 60 * 10


@require_http_methods(["GET", "POST"])
def user_login_view(request: HttpRequest) -> HttpResponse:
    """Handles user form submission and save data to session and cookies."""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            age = form.cleaned_data["age"]

            request.session["age"] = age

            response = redirect("session:greeting")
            response.set_cookie(
                "name",
                name,
                max_age=COOKIE_MAX_AGE,
                httponly=True,
                samesite="Lax",
            )
            return response
    else:
        form = LoginForm()
    return render(request, "session/login.html", {"form": form})


def greeting_view(request: HttpRequest) -> HttpResponse:
    """Displays greeting page using session and cookies data."""
    name = request.COOKIES.get("name")
    age = request.session.get("age")

    if not name or not age:
        messages.warning(request, "Your session or cookies expired.")
        return redirect("session:login")

    response = render(
        request,
        "session/greeting.html",
        {
            "name": name,
            "age": age,
        },
    )

    response.set_cookie("name",
                        name, max_age=COOKIE_MAX_AGE,
                        httponly=True,
                        samesite="Lax")
    return response


def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    """Clears session and cookies data."""
    request.session.flush()
    response = redirect("session:login")
    response.delete_cookie("name")
    return response

def unoptimized_books_view(request: HttpRequest) -> HttpResponse:
    """Displays books list without ORM optimization."""
    start = time.perf_counter()
    books = BookData.objects.all()
    result = []

    for book in books:
        result.append({
            "title": book.title,
            "author": book.author.name,
            "reviews": [review.text for review in book.reviews.all()],
        })

    execution_time = time.perf_counter() - start
    return render(
        request,
        "session/book_list.html",
        {
            "books": result,
            "execution_time": execution_time,
            "query_count": len(connection.queries),
        },
    )


def optimized_books_view(request: HttpRequest) -> HttpResponse:
    """Displays books list with ORM optimization."""
    start = time.perf_counter()
    books = BookData.objects.select_related("author").prefetch_related("reviews")
    result = []

    for book in books:
        result.append({
            "title": book.title,
            "author": book.author.name,
            "reviews": [review.text for review in book.reviews.all()],
        })

    execution_time = time.perf_counter() - start
    return render(
        request,
        "session/book_list.html",
        {
            "books": result,
            "execution_time": execution_time,
            "query_count": len(connection.queries),
        },
    )


def cached_books_view(request: HttpRequest) -> HttpResponse:
    """Displays cached books list."""
    cache_key = "book_list_with_authors"
    books = cache.get(cache_key)

    if books is None:
        books = list(
            BookData.objects.select_related("author")
            .prefetch_related("reviews")
        )
        cache.set(cache_key, books, timeout=60 * 5)

    return render(request,"session/book_list.html",{"books": books})


def statistics_view(request: HttpRequest) -> HttpResponse:
    """Displays statistics using annotations and aggregations."""
    authors = Author.objects.annotate(
        average_rating=Avg("books__reviews__rating"),
        books_count=Count("books"),
    )
    books = BookData.objects.select_related("author").annotate(
        reviews_count=Count("reviews"),
        average_rating=Avg("reviews__rating"),
    ).order_by("-reviews_count", "-average_rating")

    return render(
        request,
        "session/statistics.html",
        {
            "authors": authors,
            "books": books,
        },
    )

def raw_sql_view(request: HttpRequest) -> HttpResponse:
    """Executes raw SQL query for authors statistics."""
    min_reviews = int(request.GET.get("min_reviews", 10))

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT a.id, a.name, COUNT(r.id) AS reviews_count
            FROM session_author a
            JOIN session_book b ON b.author_id = a.id
            JOIN session_review r ON r.book_id = b.id
            GROUP BY a.id, a.name
            HAVING COUNT(r.id) > %s
            """,
            [min_reviews],
        )
        authors = cursor.fetchall()

    return render(
        request,
        "session/statistics.html",
        {"raw_authors": authors},
    )

def task_status_view(request: HttpRequest, task_id: str) -> HttpResponse:
    """Displays Celery task status."""
    result = AsyncResult(task_id)
    return render(
        request,
        "session/task_status.html",
        {
            "task_id": task_id,
            "status": result.status,
            "result": result.result if result.ready() else None,
        },
    )
