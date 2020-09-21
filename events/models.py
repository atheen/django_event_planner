from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    date = models.DateField()
    tickets = models.PositiveIntegerField()
    available_tickets = models.PositiveIntegerField()
    booked_tickets = models.PositiveIntegerField(default=0)
    planner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Attendee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reserved_tickets = models.PositiveIntegerField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees')
