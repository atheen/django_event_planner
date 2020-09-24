from rest_framework import serializers
from django.contrib.auth.models import User

from events.models import Event,Attendee

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name','description','date','tickets','available_tickets','planner']

class AttendeeSerializer(serializers.ModelSerializer):
    event = serializers.SerializerMethodField()
    class Meta:
        model = Attendee
        fields = ['event','reserved_tickets']

    def get_event(self,obj):
        return "%s - (%s)"%(obj.event.name,obj.event.date)

class AttendeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['user']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        new_user = User(username=username)
        new_user.set_password(password)
        new_user.save()
        return validated_data
