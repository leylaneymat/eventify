from rest_framework import serializers

from events.models import Comment, Event, Like, SavedEvent, Ticket


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
    category = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "date",
            "name",
            "description",
            "tickets",
            "comments",
            "likes",
            "category",  # <-- added here
        )

    def get_likes(self, obj):
        return obj.likes.count()

    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets", None)
        # If category is included in validated_data it will be present here
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


class SavedEventSerializer(serializers.ModelSerializer):
    """Serializer for saving/unsaving events"""

    event_id = serializers.IntegerField(write_only=True)
    event = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SavedEvent
        fields = ["id", "event_id", "event", "saved_at"]
        read_only_fields = ["id", "saved_at"]

    def get_event(self, obj):
        # Import your existing EventSerializer here
        from events.api.serializers import EventSerializer

        return EventSerializer(obj.event).data

    def create(self, validated_data):
        user = self.context["request"].user
        event_id = validated_data.pop("event_id")

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise serializers.ValidationError({"event_id": "Event not found"})

        saved_event, created = SavedEvent.objects.get_or_create(user=user, event=event)

        if not created:
            raise serializers.ValidationError({"detail": "Event already saved"})

        return saved_event


class SavedEventListSerializer(serializers.ModelSerializer):
    """Serializer for listing saved events"""

    event = serializers.SerializerMethodField()

    class Meta:
        model = SavedEvent
        fields = ["id", "event", "saved_at"]

    def get_event(self, obj):
        # Import your existing EventSerializer here
        from events.api.serializers import EventSerializer

        return EventSerializer(obj.event).data
