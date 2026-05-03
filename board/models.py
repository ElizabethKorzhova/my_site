"""Module containing model definitions for board application."""
from datetime import timedelta
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class CustomUser(models.Model):
    """Model definition for CustomUser based on Django's User model.
    CustomUser and Category have One-to-Many relationship.

        Fields:
            username: required and unique;
            password: required;
            phone (CharField): required and unique;
            address (CharField): required."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, unique=True)
    address = models.CharField(max_length=50)

    def __str__(self):
        """Return username as a string representation of CustomUser class."""
        return self.user.username


class Category(models.Model):
    """Model definition for Category based on Django's Model.
    Category and Ad have One-to-Many relationship.

        Fields:
            name (CharField): required and unique;
            description (TextField): required."""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        """Return name as a string representation of Category class."""
        return self.name

    def get_count_active_ads(self) -> int:
        """Return count of active ads in the category."""
        return self.ads.filter(is_active=True).count()


class Ad(models.Model):
    """Model definition for Ad (Advertisement) based on Django's Model.
    Category and Ad have One-to-Many relationship.
    CustomUser and Category have One-to-Many relationship.

        Fields:
            title (CharField): required and unique;
            description (TextField): required.
            price (DecimalField): required;
            created_at (DateTimeField): required;
            updated_at (DateTimeField): required;
            is_active (BooleanField): required;
            user (ForeignKey) references CustomUser;
            category (ForeignKey) references Category."""
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="ads")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="ads")

    def __str__(self):
        """Return title as a string representation of Ad class."""
        return self.title

    def get_short_description(self) -> str:
        """Return the shortened version of the description (up to 100 characters)."""
        if len(self.description) > 100:
            return self.description[:100] + "..."
        return self.description

    def deactivate(self) -> None:
        """Deactivate the active ad 30 days after it is created."""
        if self.is_active and (timezone.now() - self.created_at) > timedelta(days=30):
            self.is_active = False
            self.save()


class Comment(models.Model):
    """Model definition for Comment based on Django's Model.
    Ad and Comment have One-to-Many relationship. CustomUser and Comment have One-to-Many relationship.

        Fields:
            content (TextField): required;
            created_at (DateTimeField): required.
            ad (ForeignKey) references Ad;
            user (ForeignKey) references CustomUser;"""
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        """Return content as a string representation of Comment class."""
        return self.content
