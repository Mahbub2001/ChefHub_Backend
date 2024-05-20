from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Event
from .serializers import EventSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user.chef)


class PublicEventListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Event.objects.all()
    serializer_class = EventSerializer