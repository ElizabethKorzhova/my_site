"""This module contains views for customization app."""
from typing import Any, Dict

from django.db.models import QuerySet
from django.http import JsonResponse, HttpRequest
from django.views import View
from django.views.generic import ListView, TemplateView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .metrics import get_requests_count
from .models import TaskInfo
from .permissions import IsTaskOwner
from .serializers import TaskInfoSerializer
from .services import users_tasks_statistics


class TaskInfoListView(ListView):
    """Class-based view for displaying task list."""
    model = TaskInfo
    template_name = "customization/tasks.html"
    context_object_name = "tasks"
    ordering = ("-created_at",)


class UsersStatisticsView(TemplateView):
    """Display users statistics page."""
    template_name = "customization/statistics.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Returns template context."""
        context = super().get_context_data(**kwargs)
        context["users_statistics"] = users_tasks_statistics()
        return context


class ServerMetricsView(View):
    """Returns server request metrics."""
    @staticmethod
    def get(request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        """Returns requests count."""
        return JsonResponse(
            {
                "requests_count": get_requests_count(),
            }
        )


class TaskInfoListAPIView(ListAPIView):
    """API view for displaying filtered task list."""
    serializer_class = TaskInfoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[TaskInfo]:
        """Returns filtered tasks queryset."""
        queryset = TaskInfo.objects.filter(owner=self.request.user)

        status = self.request.query_params.get("status")
        priority = self.request.query_params.get("priority")

        if status:
            queryset = queryset.filter(status=status)

        if priority:
            queryset = queryset.filter(priority=priority)

        return queryset.order_by("-created_at")


class TaskInfoDetailAPIView(RetrieveAPIView):
    """API view for displaying task detail."""
    serializer_class = TaskInfoSerializer
    permission_classes = (IsAuthenticated, IsTaskOwner)
    queryset = TaskInfo.objects.all()
