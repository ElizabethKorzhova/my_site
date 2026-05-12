"""This module contains tests for the task serializers."""
import pytest
from django.utils import timezone

from testing.serializers import TaskSerializer, TaskWithUserSerializer


@pytest.mark.django_db
def test_task_serializer_valid_data() -> None:
    """Tests that serializer is valid with correct data."""
    serializer = TaskSerializer(
        data={
            "title": "Test task",
            "description": "Some description",
            "due_date": timezone.localdate(),
        }
    )

    assert serializer.is_valid()


@pytest.mark.django_db
def test_task_serializer_title_required() -> None:
    """Tests that serializer returns error when title is missing."""
    serializer = TaskSerializer(
        data={
            "description": "Some description",
            "due_date": timezone.localdate(),
        }
    )

    assert not serializer.is_valid()
    assert "title" in serializer.errors


@pytest.mark.django_db
def test_task_serializer_due_date_cannot_be_in_past() -> None:
    """Tests that serializer returns error for past due date."""
    serializer = TaskSerializer(
        data={
            "title": "Test task",
            "description": "Some description",
            "due_date": timezone.localdate() - timezone.timedelta(days=1),
        }
    )

    assert not serializer.is_valid()
    assert "due_date" in serializer.errors


@pytest.mark.django_db
def test_task_with_user_serializer_valid_data() -> None:
    """Tests that nested serializer is valid with correct data."""
    serializer = TaskWithUserSerializer(
        data={
            "title": "Test task",
            "description": "Some description",
            "due_date": timezone.localdate(),
            "user": {
                "username": "testuser",
                "email": "test@example.com",
            },
        }
    )

    assert serializer.is_valid()


@pytest.mark.django_db
def test_task_with_user_serializer_invalid_nested_user() -> None:
    """Tests that nested serializer returns errors for invalid user data."""
    serializer = TaskWithUserSerializer(
        data={
            "title": "Test task",
            "description": "Some description",
            "due_date": timezone.localdate(),
            "user": {
                "username": "",
                "email": "not-email",
            },
        }
    )

    assert not serializer.is_valid()
    assert "user" in serializer.errors
    assert "username" in serializer.errors["user"]
    assert "email" in serializer.errors["user"]


@pytest.mark.django_db
class TestTaskSerializer:
    """Class-based tests for TaskSerializer."""

    def test_valid_data(self) -> None:
        """Tests that serializer is valid with correct data."""
        serializer = TaskSerializer(
            data={
                "title": "Test task",
                "description": "Some description",
                "due_date": timezone.localdate(),
            }
        )

        assert serializer.is_valid()

    def test_title_required(self) -> None:
        """Tests that serializer returns error when title is missing."""
        serializer = TaskSerializer(
            data={
                "description": "Some description",
                "due_date": timezone.localdate(),
            }
        )

        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_due_date_cannot_be_in_past(self) -> None:
        """Tests that serializer returns error for past due date."""
        serializer = TaskSerializer(
            data={
                "title": "Test task",
                "description": "Some description",
                "due_date": timezone.localdate() - timezone.timedelta(days=1),
            }
        )

        assert not serializer.is_valid()
        assert "due_date" in serializer.errors


@pytest.mark.django_db
class TestTaskWithUserSerializer:
    """Class-based tests for TaskWithUserSerializer."""

    def test_valid_nested_user_data(self) -> None:
        """Tests that nested serializer is valid with correct user data."""
        serializer = TaskWithUserSerializer(
            data={
                "title": "Test task",
                "description": "Some description",
                "due_date": timezone.localdate(),
                "user": {
                    "username": "testuser",
                    "email": "test@example.com",
                },
            }
        )

        assert serializer.is_valid()

    def test_invalid_nested_user_data(self) -> None:
        """Tests that nested serializer returns errors for invalid user data."""
        serializer = TaskWithUserSerializer(
            data={
                "title": "Test task",
                "description": "Some description",
                "due_date": timezone.localdate(),
                "user": {
                    "username": "",
                    "email": "wrong-email",
                },
            }
        )

        assert not serializer.is_valid()
        assert "user" in serializer.errors
