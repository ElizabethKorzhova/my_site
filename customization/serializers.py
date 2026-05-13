"""This module contains serializers for customization app."""
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import TaskComment, TaskInfo

User = get_user_model()


class UserShortSerializer(serializers.ModelSerializer):
    """Short serializer for user."""

    class Meta:
        """Meta options for UserShortSerializer."""
        model = User
        fields = ("id", "username", "email")


class TaskCommentSerializer(serializers.ModelSerializer):
    """Serializer for task comment."""

    class Meta:
        """Meta options for TaskCommentSerializer."""
        model = TaskComment
        fields = ("id", "text", "created_at")


class TaskInfoSerializer(serializers.ModelSerializer):
    """Serializer for task info with nested fields."""
    owner = UserShortSerializer(read_only=True)
    comments = TaskCommentSerializer(many=True, read_only=True)

    class Meta:
        """Meta options for TaskInfoSerializer."""
        model = TaskInfo
        fields = (
            "id",
            "title",
            "description",
            "status",
            "priority",
            "owner",
            "comments",
            "created_at",
        )
