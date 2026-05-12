"""This module contains all forms for testing application."""
import datetime

from django import forms
from django.utils import timezone

from .models import Task


class TaskForm(forms.ModelForm):
    """TaskForm for testing Task model."""
    class Meta:
        """Metaclass for TaskForm."""
        model = Task
        fields = ["title", "description", "due_date"]

    def clean_due_date(self) -> datetime.date | None:
        """Validates due date is in the future."""
        due_date = self.cleaned_data.get("due_date")

        if due_date and due_date < timezone.localdate():
            raise forms.ValidationError("Due date cannot be in the past.")

        return due_date
