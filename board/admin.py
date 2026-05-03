"""This module defines the configuration of the admin panel
 and the registration of models."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import CustomUser, Comment, Category, Ad


class CustomUserInline(admin.StackedInline):
    """Inline representation of CustomUser model for UserAdmin."""
    model = CustomUser


class UserAdmin(BaseUserAdmin):
    """Admin configuration for the User model."""
    inlines = (CustomUserInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for the Category model."""
    list_display = ("name", "get_count_active_ads")
    readonly_fields = ("id", "get_count_active_ads")

    list_filter = ("name",)
    search_fields = ("name",)
    search_help_text = "Search by category name"


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """Admin configuration for the Ad model."""
    list_display = ("title", "price", "category", "user", "is_active")
    readonly_fields = ("id", "created_at", "updated_at")

    list_filter = ("category", "is_active")
    search_fields = ("title",)
    search_help_text = "Search by ad title"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for the Comment model."""
    list_display = ("content", "ad", "user", "created_at")
    readonly_fields = ("id", "created_at",)

    search_fields = ("content",)
    search_help_text = "Search by comment content"
