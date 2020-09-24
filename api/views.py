from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from datetime import datetime
from rest_framework.permissions import IsAuthenticated

from events.models import Event,Attendee
from .serializers import EventSerializer,AttendeeSerializer,UserCreateSerializer
from .permissions import IsPlanner

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

class CreateEvent(CreateAPIView):
	serializer_class = EventSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class UpdateEvent(RetrieveUpdateAPIView):
	queryset = Event.objects.all()
	serializer_class = EventSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	permission_classes = [IsPlanner]

class AttendeeListView(RetrieveAPIView):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer
    lookup_field = 'event'
    lookup_url_kwarg = 'event_id'

class BookEvent(CreateAPIView):
	serializer_class = AttendeeSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user, event=self.kwargs['event_id'])
