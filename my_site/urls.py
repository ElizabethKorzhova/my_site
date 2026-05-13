"""
URL configuration for my_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from typing import List

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, URLPattern, URLResolver
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns: List[URLPattern | URLResolver] = [
    path("admin/", admin.site.urls),
    path("main/", include("main.urls")),
    path("board/", include("board.urls")),
    path("users/", include("users.urls")),
    path("customization/", include("customization.urls")),
    path("realtime/", include("realtime.urls")),
    path("books/api/", include("books.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("books/api/auth/token/", obtain_auth_token, name="api-token-auth"),
    path("books/api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("books/api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("books/api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("", include("home.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
