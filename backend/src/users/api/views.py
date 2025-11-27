from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.api.serializers import UserSerializer
from users.models import User
from users.permissions import AllowCreate, IsAdminOrIsOwner


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = "user_pk"
    permission_classes = [AllowCreate | IsAdminOrIsOwner]


@api_view(["GET"])
def get_user_by_username(request, username):
    if request.user.is_anonymous:  # IsAuthenticated
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    user = get_object_or_404(User, username=username)

    if not request.user.is_superuser and request.user != user:  # IsAdminOrIsOwner
        return Response(status=status.HTTP_403_FORBIDDEN)

    return Response(UserSerializer(user).data)
