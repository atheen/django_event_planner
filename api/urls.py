from django.urls import path
from .views import EventListView, PlannerEventListView, BookedEventListView, APIRegister

from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('api/events/', EventListView.as_view(), name='events-list'),
    path('api/<int:planner_id>/events/', PlannerEventListView.as_view(), name='planner-events'),
    path('api/booked-events/', BookedEventListView.as_view(), name='booked-events'),

    path('api/login/', TokenObtainPairView.as_view(), name='api-login'),
    path('api/register/',  APIRegister.as_view() , name='api-register'),
]
