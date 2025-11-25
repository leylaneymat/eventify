from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from events.api.serializers import CommentSerializer, TicketSerializer
from events.models import Comment, Event, Ticket
from events.permissions import IsAdminOrIsOwnerOrReadOnly, IsAdminOrReadOnly


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


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    lookup_url_kwarg = "comment_pk"
    permission_classes = [IsAdminOrIsOwnerOrReadOnly]

    def get_queryset(self):
        event_id = self.kwargs["event_pk"]
        event = get_object_or_404(Event, pk=event_id)
        comments = Comment.objects.filter(event_id=event_id)

        if not event and not comments:
            raise NotFound()

        return comments

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        event_id = self.kwargs["event_pk"]
        user = self.request.user
        event = get_object_or_404(Event, pk=event_id)
        serializer.save(event=event, user=user)
