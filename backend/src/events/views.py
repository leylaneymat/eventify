from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from events.api.serializers import SavedEventListSerializer, SavedEventSerializer
from events.models import Event, SavedEvent


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
