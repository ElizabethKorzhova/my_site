"""This module defines the configuration of the admin panel
 and the registration of models."""
from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin configuration for the Task model."""
    list_display = ("title", "due_date", "user")
    readonly_fields = ("id",)

    search_fields = ("title",)
    search_help_text = "Search by task title"
