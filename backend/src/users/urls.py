from django.urls import path

from users.api.views import (
    PurchasedTicketViewSet,
    UserViewSet,
    get_user_by_username,
    send_ticket_receipt,
)

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
    # purchased tickets
    path(
        "<int:user_pk>/purchased_tickets/",
        PurchasedTicketViewSet.as_view(
            {"get": "list", "post": "create"},
            suffix="List",
        ),
    ),
    path(
        "<int:user_pk>/purchased_tickets/<int:purchased_ticket_pk>/",
        PurchasedTicketViewSet.as_view(
            {"get": "retrieve"},
            suffix="Instance",
        ),
    ),
    path(
        "purchased_tickets/<int:purchased_ticket_id>/send_receipt/",
        send_ticket_receipt,
        name="send-ticket-receipt",
    ),
]
