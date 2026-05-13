"""URL configuration for customization app."""
from typing import List

from django.urls import path, URLPattern, URLResolver

from .views import (TaskInfoListView, UsersStatisticsView, ServerMetricsView, TaskInfoListAPIView,
                    TaskInfoDetailAPIView)

urlpatterns: List[URLPattern | URLResolver] = [
    path("tasks/", TaskInfoListView.as_view(), name="tasks_list"),
    path("statistics/", UsersStatisticsView.as_view(), name="statistics"),
    path("metrics/", ServerMetricsView.as_view(), name="server_metrics"),
    path("api/tasks/", TaskInfoListAPIView.as_view(), name="api_tasks_list"),
    path("api/tasks/<int:pk>/", TaskInfoDetailAPIView.as_view(), name="api_task_detail"),
]
