"""Module containing model definitions for testing application."""
from django.conf import settings
from django.db import models


class Task(models.Model):
    """Model definition for Task.

            Fields:
                title (CharField): required;
                description (TextField): not required;
                due_date (DateField): required;
                user (ForeignKey): required;"""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks", )

    def __str__(self) -> str:
        return self.title
