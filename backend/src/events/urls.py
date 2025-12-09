from django.urls import path

from events.api.views import EventViewSet, TicketViewSet, LikeViewSet, CommentViewSet


urlpatterns = [
    # events
    path(
        "", 
        EventViewSet.as_view(
            {"get": "list", "post": "create"},
            suffix='List',
        ),
    ),
    path(
        "<int:event_pk>/",
        EventViewSet.as_view(
            {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"},
            suffix='Instance',
        ),
    ),
    
    # tickets
    path(
        "<int:event_pk>/tickets/",
        TicketViewSet.as_view(
            {"get": "list", "post": "create"},
            suffix='List',
        ),
    ),
    path(
        "<int:event_pk>/tickets/<int:ticket_pk>/",
        TicketViewSet.as_view(
            {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"},
            suffix='Instance',
        ),
    ),
    
    # likes
    path(
        "<int:event_pk>/likes/",
        LikeViewSet.as_view(
            {"get": "list", "post": "create"},
            suffix='List',
        ),
    ),
    path(
        "<int:event_pk>/likes/<int:like_pk>/",
        LikeViewSet.as_view(
            {"get": "retrieve", "delete": "destroy"},
            suffix='Instance',
        ),
    ),
    
    # comments
    path(
        "<int:event_pk>/comments/",
        CommentViewSet.as_view(
            {"get": "list", "post": "create"},
            suffix='List',
        ),
    ),
    path(
        "<int:event_pk>/comments/<int:comment_pk>/",
        CommentViewSet.as_view(
            {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"},
            suffix='Instance',
        ),
    ),
]
