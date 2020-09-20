from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.models import User

from .forms import UserSignup, UserLogin, EventForm, BookEventForm, ProfileUpdate
from .models import Event,Attendee

def home(request):
    return render(request, 'home.html')

class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('dashboard')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")



#STARTED

def update_profile(request,user_id):
    user_obj = User.objects.get(id=user_id)
    if request.user != user_obj:
        messages.success(request, "You have no access.")
    else:
        form = ProfileUpdate(instance=user_obj)
        if request.method == 'POST':
            form = ProfileUpdate(request.POST, instance=user_obj)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
    context = {
        "user": user_obj,
        "form": form
    }
    return render(request, 'profile_update.html', context)




def dashboard(request):
    context = {
        "planned_events":Event.objects.filter(planner=request.user),
        "attended_events":Attendee.objects.filter(user=request.user),
    }
    return render(request,'dashboard.html',context)

def event_details(request,event_id):
    event_obj = Event.objects.get(id=event_id)
    context = {
        "event": event_obj,
        "attendees": event_obj.attendees.all()
    }
    return render(request,'event_details.html',context)

def event_update(request,event_id):
    event_obj = Event.objects.get(id=event_id)
    form = EventForm(instance=event_obj)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event_obj)
        if form.is_valid():
            form.save()
            return redirect('event-details',event_id)
    context = {
        "event": event_obj,
        "form": form,
    }
    return render(request, 'event_update.html', context)

def events_list(request):
    if request.user.is_anonymous:
        return redirect('login')
    context = {
        "events": Event.objects.filter(date__gte=datetime.today())
    }
    return render(request, 'events_list.html',context)

def create_event(request):
    if request.user.is_anonymous:
        return redirect('login')
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.planner = request.user
            obj.save()
            return redirect('dashboard')
    context = {
        "form": form,
    }
    return render(request, 'create_event.html',context)

def book_event(request, event_id):
    if request.user.is_anonymous:
        return redirect('login')
    event_obj = Event.objects.get(id=event_id)
    form = BookEventForm()
    if request.method == "POST":
        form = BookEventForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.event = event_obj
            obj.user = request.user
            obj.save()
            return redirect('dashboard')
    context = {
        "event": event_obj,
        "form": form
    }
    return render(request, 'book_event.html', context)
