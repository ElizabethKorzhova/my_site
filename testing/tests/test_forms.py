"""This module contains tests for the TaskForm."""
from datetime import timedelta

import pytest
from django.utils import timezone

from testing.forms import TaskForm


@pytest.mark.django_db
def test_task_form_valid_data() -> None:
    """Tests that form is valid with correct data."""
    form = TaskForm(
        data={
            "title": "Test task",
            "description": "Test description",
            "due_date": timezone.localdate(),
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_task_form_required_title_error() -> None:
    """Tests that form returns error when title is empty."""
    form = TaskForm(
        data={
            "title": "",
            "description": "Some description",
            "due_date": timezone.localdate(),
        }
    )

    assert not form.is_valid()
    assert "title" in form.errors


@pytest.mark.django_db
def test_task_form_due_date_cannot_be_in_past() -> None:
    """Tests that form returns error for past due date."""
    form = TaskForm(
        data={
            "title": "Test task",
            "description": "Some description",
            "due_date": timezone.localdate() - timedelta(days=1),
        }
    )

    assert not form.is_valid()
    assert "due_date" in form.errors


@pytest.mark.django_db
class TestTaskForm:
    """Class-based tests for TaskForm."""

    def test_valid_data(self) -> None:
        """Tests that form is valid with correct data."""
        form = TaskForm(
            data={
                "title": "Test task",
                "description": "Test description",
                "due_date": timezone.localdate(),
            }
        )

        assert form.is_valid()

    def test_empty_required_title(self) -> None:
        """Tests that form returns error when title is empty."""
        form = TaskForm(
            data={
                "title": "",
                "description": "Some description",
                "due_date": timezone.localdate(),
            }
        )

        assert not form.is_valid()
        assert "title" in form.errors

    def test_due_date_in_past(self) -> None:
        """Tests that form returns error for past due date."""
        form = TaskForm(
            data={
                "title": "Test task",
                "description": "Some description",
                "due_date": timezone.localdate() - timedelta(days=1),
            }
        )

        assert not form.is_valid()
        assert "due_date" in form.errors
