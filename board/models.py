"""Module containing model definitions for board application."""
from django.db import models
from django.contrib.auth.models import User


class CustomUser(User):
    """Model definition for CustomUser based on Django's User model.
    CustomUser and Category have One-to-Many relationship.

        Fields:
            username: required and unique;
            password: required;
            phone (CharField): required and unique;
            address (CharField): required."""
    phone = models.CharField(max_length=12, unique=True)
    address = models.CharField(max_length=50)


class Category(models.Model):
    """Model definition for Category based on Django's Model.
    Category and Ad have One-to-Many relationship.

        Fields:
            name (CharField): required and unique;
            description (TextField): required."""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()


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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


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
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
