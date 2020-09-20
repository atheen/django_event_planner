from django import forms
from django.contrib.auth.models import User

from .models import Event,Attendee

class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }


class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['planner']
        # fields = "__all__"

class BookEventForm(forms.ModelForm):
    class Meta:
        model = Attendee
        exclude = ['user','event']
        # fields = "__all__"
