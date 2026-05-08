"""This module defines the configuration of the admin panel
 and the registration of models."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """Inline representation of UserProfileInline model for UserAdmin."""
    model = UserProfile


class UserAdmin(BaseUserAdmin):
    """Admin configuration for the User model."""
    inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
