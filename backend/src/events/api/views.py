from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from events.api.serializers import (
    CommentSerializer,
    EventSerializer,  # Make sure you import your serializer
    LikeSerializer,
    SavedEventListSerializer,
    SavedEventSerializer,
    TicketSerializer,
)
from events.models import Comment, Event, Like, SavedEvent, Ticket
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


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    lookup_url_kwarg = "like_pk"
    permission_classes = [IsAdminOrIsOwnerOrReadOnly]

    def get_queryset(self):
        event_id = self.kwargs["event_pk"]
        event = get_object_or_404(Event, pk=event_id)
        likes = Like.objects.filter(event_id=event_id)

        if not event and not likes:
            raise NotFound()

        return likes

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        event_id = self.kwargs["event_pk"]
        event = get_object_or_404(Event, pk=event_id)

        try:
            serializer.save(event=event, user=user)
        except IntegrityError:
            raise ValidationError("You have already liked this event.")


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAdminOrReadOnly]
    lookup_url_kwarg = "event_pk"

    def get_queryset(self):
        qs = Event.objects.all()
        category = self.request.query_params.get("category")
        if not category:
            return qs
        # allow comma-separated list: ?category=concert or ?category=concert,festival
        cats = [c.strip() for c in category.split(",") if c.strip()]
        return qs.filter(category__in=cats)


class SaveEventView(APIView):
    """
    POST: Save an event for the authenticated user
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SavedEventSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnsaveEventView(APIView):
    """
    DELETE: Remove an event from user's saved list
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, event_id):
        saved_event = get_object_or_404(
            SavedEvent, user=request.user, event_id=event_id
        )
        saved_event.delete()
        return Response(
            {"detail": "Event removed from saved list"},
            status=status.HTTP_204_NO_CONTENT,
        )


class SavedEventsListView(generics.ListAPIView):
    """
    GET: List all saved events for the authenticated user
    """

    permission_classes = [IsAuthenticated]
    serializer_class = SavedEventListSerializer

    def get_queryset(self):
        return SavedEvent.objects.filter(user=self.request.user).select_related("event")


class CheckEventSavedView(APIView):
    """
    GET: Check if an event is saved by the authenticated user
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        is_saved = SavedEvent.objects.filter(
            user=request.user, event_id=event_id
        ).exists()
        return Response({"is_saved": is_saved}, status=status.HTTP_200_OK)
