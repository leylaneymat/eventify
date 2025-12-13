from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import PurchasedTicket, User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class PurchasedTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasedTicket
        fields = (
            "id",
            "event",
            "ticket",
            "user",
            "purchase_date",
        )
        read_only_fields = ("user", "purchase_date")
