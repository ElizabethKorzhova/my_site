"""This module contains custom context processors."""
from typing import Dict

from django.http import HttpRequest

from .models import TaskInfo


def global_tasks_data(request: HttpRequest) -> Dict[str, int]:
    """Adds global tasks data to template context."""
    return {
        "global_tasks_count": TaskInfo.objects.count(),
        "global_done_tasks_count": TaskInfo.objects.filter(status="done").count(),
    }
