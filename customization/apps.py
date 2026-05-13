"""Application configuration for customization app."""
from django.apps import AppConfig


class CustomizationConfig(AppConfig):
    """Configuration for customization app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "customization"

    def ready(self) -> None:
        """Imports signals."""
        import customization.signals
