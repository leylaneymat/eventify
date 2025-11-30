from rest_framework import serializers

from events.models import Comment, Event, Like, Ticket


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


class EventSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "description",
            "tickets",
            "comments",
            "likes",
        )

    def get_likes(self, obj):
        return obj.likes.count()

    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets", None)
        event = Event.objects.create(**validated_data)

        if tickets_data:
            for ticket_data in tickets_data:
                Ticket.objects.create(event=event, **ticket_data)

        return event


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            "id",
            "event",
            "user",
        )
        read_only_fields = ("event", "user")
