"""This module contains custom permissions for customization app."""
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import TaskInfo


class IsTaskOwner(BasePermission):
    """Allow access only to task owner."""

    def has_object_permission(self, request: Request, view: APIView, obj: TaskInfo) -> bool:
        """Checks if user is task owner."""
        return obj.owner == request.user
