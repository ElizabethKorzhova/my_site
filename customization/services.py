"""This module contains database query services."""
from django.contrib.auth import get_user_model
from django.db.models import Count, QuerySet

User = get_user_model()


def users_tasks_statistics() -> QuerySet[User]:
    """Returns users with total tasks count."""
    return User.objects.annotate(
        tasks_count=Count("tasks_info"),
    ).order_by("-tasks_count")
