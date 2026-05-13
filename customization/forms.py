"""This module contains forms for customization application."""
import re
from typing import Any

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import TaskInfo, UserContactInfo


User = get_user_model()


def validate_task_title(value: str) -> None:
    """Validates task title."""
    if len(value.strip()) < 3:
        raise forms.ValidationError("Title must contain at least 3 characters.")

    if value[0].isdigit():
        raise forms.ValidationError("Title cannot start with a number.")


class PhoneNumberField(forms.CharField):
    """Custom form field for validating phone number."""

    def validate(self, value: str) -> None:
        """Validates phone number format."""
        super().validate(value)

        if value and not re.fullmatch(r"^\+?\d{10,15}$", value):
            raise forms.ValidationError(
                "Enter a valid phone number. Example: +380991234567."
            )


class PrioritySelect(forms.Select):
    """Custom select widget for priority field."""
    template_name = "customization/widgets/priority_select.html"


class TaskInfoForm(forms.ModelForm):
    """Form for creating and updating task info."""
    title = forms.CharField(max_length=255, validators=[validate_task_title],)

    class Meta:
        """Meta options for TaskInfoForm."""
        model = TaskInfo
        fields = (
            "title",
            "description",
            "status",
            "priority",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "priority": PrioritySelect(),
        }


class RegistrationForm(UserCreationForm):
    """User registration form with custom validation."""
    email = forms.EmailField(required=True)
    phone_number = PhoneNumberField(required=False)

    class Meta:
        """Meta options for RegistrationForm."""
        model = User
        fields = (
            "username",
            "email",
            "phone_number",
            "password1",
            "password2",
        )

    def clean_email(self) -> str:
        """Validates unique user email."""
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email already exists.")

        return email

    def clean_username(self) -> str:
        """Validates unique username."""
        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("User with this username already exists.")

        return username

    def save(self, commit: bool = True) -> Any:
        """Saves user and related contact info."""
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            UserContactInfo.objects.create(
                user=user,
                phone_number=self.cleaned_data.get("phone_number", ""),
            )

        return user
