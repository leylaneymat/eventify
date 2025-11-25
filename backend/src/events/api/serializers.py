from rest_framework import serializers

from events.models import Ticket


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
