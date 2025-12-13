import logging

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.api.serializers import PurchasedTicketSerializer, UserSerializer
from users.models import PurchasedTicket, User
from users.permissions import AllowCreate, IsAdminOrIsOwner


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = "user_pk"
    permission_classes = [AllowCreate | IsAdminOrIsOwner]


class PurchasedTicketViewSet(viewsets.ModelViewSet):
    serializer_class = PurchasedTicketSerializer
    lookup_url_kwarg = "purchased_ticket_pk"
    permission_classes = [IsAdminOrIsOwner]

    def get_queryset(self):
        user_pk = self.kwargs["user_pk"]
        user = get_object_or_404(User, pk=user_pk)
        purchased_tickets = PurchasedTicket.objects.filter(user=user_pk)

        if not user and not purchased_tickets:
            raise NotFound()

        return purchased_tickets

    def perform_create(self, serializer):
        user_pk = self.kwargs["user_pk"]
        user = get_object_or_404(User, pk=user_pk)

        if (
            not self.request.user.is_staff
            and user != self.request.user
            or not self.request.user.is_authenticated
        ):
            raise PermissionDenied()

        serializer.save(user=user)


@api_view(["GET"])
def get_user_by_username(request, username):
    if request.user.is_anonymous:  # IsAuthenticated
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    user = get_object_or_404(User, username=username)

    if not request.user.is_superuser and request.user != user:  # IsAdminOrIsOwner
        return Response(status=status.HTTP_403_FORBIDDEN)

    return Response(UserSerializer(user).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_ticket_receipt(request, purchased_ticket_id):
    """Send receipt email for a purchased ticket"""
    try:
        purchased_ticket = PurchasedTicket.objects.select_related(
            "user", "event", "ticket"
        ).get(id=purchased_ticket_id, user=request.user)

        user_email = request.user.email
        if not user_email:
            return Response(
                {"error": "No email address found for user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        context = {
            "user": request.user,
            "event": purchased_ticket.event,
            "ticket": purchased_ticket.ticket,
            "purchase_date": purchased_ticket.purchase_date,
            "purchased_ticket_id": purchased_ticket.id,
        }

        subject = f"Ticket Receipt - {purchased_ticket.event.name}"
        html_message = render_to_string("emails/ticket_receipt.html", context)
        plain_message = render_to_string("emails/ticket_receipt.txt", context)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )

        return Response(
            {"message": f"Receipt sent to {user_email}"},
            status=status.HTTP_200_OK,
        )

    except PurchasedTicket.DoesNotExist:
        return Response(
            {"error": "Purchased ticket not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    except Exception:
        # 👇 Logs full traceback to console
        logger = logging.getLogger(__name__)
        logger.exception(
            "Failed to send ticket receipt",
            extra={
                "user_id": request.user.id,
                "purchased_ticket_id": purchased_ticket_id,
            },
        )

        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
