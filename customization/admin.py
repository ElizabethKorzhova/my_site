"""This module defines the configuration of the admin panel
 and the registration of models."""
from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import TaskInfo, TaskComment, UserContactInfo


class TaskCommentInline(admin.TabularInline):
    """Inline admin for displaying task comments inside task admin."""
    model = TaskComment
    extra = 1
    readonly_fields = ("created_at",)


@admin.action(description="Mark selected tasks as done")
def mark_tasks_as_done(
        modeladmin: admin.ModelAdmin,
        request: HttpRequest,
        queryset: QuerySet[TaskInfo],
) -> None:
    """Marks selected tasks as done."""
    queryset.update(status="done")


@admin.action(description="Mark selected tasks as high priority")
def mark_tasks_as_high_priority(
        modeladmin: admin.ModelAdmin,
        request: HttpRequest,
        queryset: QuerySet[TaskInfo],
) -> None:
    """Marks selected tasks as high priority."""
    queryset.update(priority="high")


@admin.register(TaskInfo)
class TaskAdmin(admin.ModelAdmin):
    """Admin configuration for TaskInfo model."""
    list_display = (
        "title",
        "owner",
        "status",
        "priority",
        "comments_count",
        "created_at",
    )
    list_filter = ("status", "priority", "created_at")
    search_fields = ("title", "description", "owner__username")
    search_help_text = "Search by task title, description and owner username"
    readonly_fields = ("id", "created_at",)
    ordering = ("-created_at",)
    inlines = (TaskCommentInline,)
    actions = (
        mark_tasks_as_done,
        mark_tasks_as_high_priority,
    )


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    """Admin configuration for TaskComment model."""
    list_display = ("task", "text", "created_at")
    list_filter = ("created_at",)
    search_fields = ("text", "task__title")
    search_help_text = "Search by text comment and task title"
    readonly_fields = ("id", "created_at",)
    ordering = ("-created_at",)


@admin.register(UserContactInfo)
class UserContactInfoAdmin(admin.ModelAdmin):
    """Admin configuration for UserContactInfo model."""
    list_display = ("user", "phone_number")
    readonly_fields = ("id",)
    search_fields = ("user__username", "user__email", "phone_number")
    search_help_text = "Search by username, email and phone number"
