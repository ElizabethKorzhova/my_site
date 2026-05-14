"""This module contains tasks Celery tasks for session app."""
import csv

from celery import shared_task
from django.core.mail import send_mail

from .models import Author, BookData


@shared_task
def import_books_from_csv(file_path: str, user_email: str) -> str:
    """Imports books data from CSV file."""
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            author, _ = Author.objects.get_or_create(name=row["author"])

            BookData.objects.get_or_create(
                title=row["title"],
                author=author,
                defaults={
                    "published_year": row.get("published_year") or None,
                },
            )

    send_mail(
        subject="CSV import completed",
        message="Books were successfully imported.",
        from_email=None,
        recipient_list=[user_email],
    )

    return "Import completed"
