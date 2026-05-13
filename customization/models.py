"""Module containing model definitions for customization application."""
from django.conf import settings
from django.db import models


class UserContactInfo(models.Model):
    """
    Model definition for UserContactInfo.

    Fields:
        user (OneToOneField): related user, required;
        phone_number (CharField): not required;.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contact_info",
    )
    phone_number = models.CharField(max_length=20, blank=True)


class UpperCaseCharField(models.CharField):
    """Represents character field with upper case."""

    def get_prep_value(self, value):
        """CharField that stores value in uppercase."""
        value = super().get_prep_value(value)

        if value is not None:
            return str(value).upper()

        return value


class TaskInfo(models.Model):
    """Model definition for TaskInfo.

            Fields:
                title (UpperCaseCharField): required;
                description (TextField): not required;
                status (CharField): required;
                priority (CharField): required;
                owner (ForeignKey): required;
                created_at (DateTimeField): auto created date;"""
    title = UpperCaseCharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("todo", "To Do"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
        ],
        default="todo",
    )
    priority = models.CharField(
        max_length=20,
        choices=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        default="medium",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks_info",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def comments_count(self) -> int:
        """Return total comments count for task."""
        return self.comments.count()

    def __str__(self) -> str:
        """String representation of Task model."""
        return self.title


class TaskComment(models.Model):
    """Model definition for TaskComment.

            Fields:
                task (ForeignKey): required;
                text (TextField): required;
                created_at (DateTimeField): auto created date;"""
    task = models.ForeignKey(
        TaskInfo,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """String representation of TaskComment model."""
        return self.text
