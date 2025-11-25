from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from events.api.serializers import TicketSerializer
from events.models import Event, Ticket
from events.permissions import IsAdminOrReadOnly


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    lookup_url_kwarg = "ticket_pk"
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        event_id = self.kwargs["event_pk"]
        event = get_object_or_404(Event, pk=event_id)
        tickets = Ticket.objects.filter(event_id=event_id)

        if not event and not tickets:
            raise NotFound()

        return tickets

    def perform_create(self, serializer):
        event_id = self.kwargs["event_pk"]
        event = get_object_or_404(Event, pk=event_id)
        serializer.save(event=event)
