"""Module containing model definitions for books application."""
from django.db import models


class Book(models.Model):
    """Model definition for Book.

            Fields:
                title: required;
                author: required;
                genre: required;
                publication_year (PositiveIntegerField): required;
                created_at (DateTimeField): auto created date;"""
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    publication_year = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
