"""
URL configuration for eventfy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.conf import settings
from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

auth = [
    path("", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

resources = [
    path("users/", include("users.urls")),
    path("events/", include("events.urls")),
    path("token/", include(auth)),
]

api_v1 = [
    path("v1/", include(resources)),
]

urlpatterns = [
    path("api/", include(api_v1)),
    path("admin/", admin.site.urls),
    path("", include("eventfy.docs")),
    path("accounts/", include("rest_framework.urls")),
]


def custom_404(request, exception=None):
    return JsonResponse({"detail": "Not found"}, status=404)


handler404 = custom_404

if settings.DEBUG is False:

    def custom_500(request):
        return JsonResponse({"detail": "Server error"}, status=500)

    handler500 = custom_500
