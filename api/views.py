from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from datetime import datetime

from events.models import Event,Attendee
from .serializers import EventSerializer,AttendeeSerializer,UserCreateSerializer

class APIRegister(CreateAPIView):
    serializer_class = UserCreateSerializer

class EventListView(ListAPIView):
    today = datetime.today()
    queryset = Event.objects.filter(date__gt=today)
    serializer_class = EventSerializer

class PlannerEventListView(ListAPIView):
    serializer_class = EventSerializer
    def get_queryset(self):
        planner = self.kwargs['planner_id']
        return Event.objects.filter(planner=planner)

class BookedEventListView(ListAPIView):
    serializer_class = AttendeeSerializer
    def get_queryset(self):
        user = self.request.user
        return Attendee.objects.filter(user=user)
