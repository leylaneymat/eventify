from django.urls import path

from users.api.views import UserViewSet, get_user_by_username

urlpatterns = [
    # users
    path(
        "",
        UserViewSet.as_view(
            {"get": "list", "post": "create"},
            suffix="List",
        ),
    ),
    path(
        "<int:user_pk>/",
        UserViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            },
            suffix="Instance",
        ),
    ),
    path("<slug:username>/", get_user_by_username),
]
