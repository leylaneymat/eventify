from django.urls import path

from events.api.views import CommentViewSet, TicketViewSet

urlpatterns = [
    # tickets
    path(
        "<int:event_pk>/tickets/",
        TicketViewSet.as_view(
            {"get": "list", "post": "create"},
            suffix="List",
        ),
    ),
    path(
        "<int:event_pk>/tickets/<int:ticket_pk>/",
        TicketViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            },
            suffix="Instance",
        ),
    ),
    # comments
    path(
        "<int:event_pk>/comments/",
        CommentViewSet.as_view(
            {"get": "list", "post": "create"},
            suffix="List",
        ),
    ),
    path(
        "<int:event_pk>/comments/<int:comment_pk>/",
        CommentViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            },
            suffix="Instance",
        ),
    ),
]
