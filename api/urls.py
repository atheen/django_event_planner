from django.urls import path
from .views import EventListView, PlannerEventListView, BookedEventListView, APIRegister, UpdateEvent, CreateEvent, AttendeeListView, BookEvent

from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('api/events/', EventListView.as_view(), name='api-events-list'),
    path('api/<int:planner_id>/events/', PlannerEventListView.as_view(), name='api-planner-events'),
    path('api/booked-events/', BookedEventListView.as_view(), name='api-booked-events'),

    path('api/login/', TokenObtainPairView.as_view(), name='api-login'),
    path('api/register/',  APIRegister.as_view() , name='api-register'),
    path('api/event/update/<int:event_id>/', UpdateEvent.as_view(), name="api-update-event"),
    path('api/event/create/',  CreateEvent.as_view() , name='api-create-event'),
    path('api/event/<int:event_id>/attendees/',  AttendeeListView.as_view() , name='api-attendee-list'),
    path('api/event/<int:event_id>/book/',  BookEvent.as_view() , name='api-book-event'),
]
