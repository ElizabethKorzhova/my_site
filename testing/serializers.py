"""This module contains serializers for testing app."""
from datetime import date

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from .models import Task


class UserSerializer(serializers.ModelSerializer):
    """Serializer for Users model."""

    class Meta:
        """Metaclass for UserSerializer."""
        model = User
        fields = ["username", "email"]


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model."""

    class Meta:
        """Metaclass for TaskSerializer."""
        model = Task
        fields = ["title", "description", "due_date"]

    @staticmethod
    def validate_due_date(value: date) -> date | None:
        """Checks that the due date is not in the past."""
        if value < timezone.localdate():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value


class TaskWithUserSerializer(TaskSerializer):
    """Serializer for TaskWithUserSerializer."""
    user = UserSerializer()

    class Meta:
        """Metaclass for TaskWithUserSerializer."""
        model = Task
        fields = TaskSerializer.Meta.fields + ["user"]
