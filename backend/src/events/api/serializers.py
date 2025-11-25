from rest_framework import serializers

from events.models import Comment, Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "name",
            "price",
            "event",
        )
        read_only_fields = ("event",)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "text",
            "event",
            "user",
        )
        read_only_fields = ("event", "user")
