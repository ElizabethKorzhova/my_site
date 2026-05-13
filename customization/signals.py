"""This module contains model signals for customization app."""
import logging
from typing import Any

from django.db.models.base import ModelBase
from django.db.models.signals import post_save
from django.dispatch import receiver

from customization.models import TaskInfo


logger = logging.getLogger(__name__)


@receiver(post_save, sender=TaskInfo)
def task_created_signal(
    sender: type[ModelBase],
    instance: TaskInfo,
    created: bool,
    **kwargs: Any,
) -> None:
    """Logs message after task creation."""
    if created:
        logger.info(
            "Task '%s' was created by user '%s'.",
            instance.title,
            instance.owner.username,
        )
