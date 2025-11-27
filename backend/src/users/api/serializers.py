from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User


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

    def create(self, validated_data):
        password = validated_data.pop("password", None)

        if not password:
            ValidationError("This field is required and cannot be empty.")

        user = self.Meta.model._default_manager.create_user(
            **validated_data, password=password
        )
        return user
