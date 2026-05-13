"""This module contains custom template tags and filters."""
from django import template

from customization.models import TaskInfo

register = template.Library()


@register.filter
def uppercase_text(value: str) -> str:
    """Returns text in uppercase."""
    if not value:
        return ""

    return str(value).upper()


@register.simple_tag
def total_tasks_count() -> int:
    """Returns total count of tasks."""
    return TaskInfo.objects.count()
