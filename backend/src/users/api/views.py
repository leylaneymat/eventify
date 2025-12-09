from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound, PermissionDenied
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
