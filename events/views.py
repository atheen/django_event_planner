from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

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

def change_password(request):
    if request.user.is_anonymous:
        return redirect('login')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated.')
            return redirect('profile-update')
        else:
            messages.error(request, 'Please correct the error.')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form':form}
    return render(request, 'change_password.html',context)


def update_profile(request):
    if request.user.is_anonymous:
        return redirect('login')
    user_obj = User.objects.get(id=request.user.id)
    if request.user != user_obj:
        messages.error(request, "You have no access.")
    else:
        form = ProfileUpdate(instance=user_obj)
        if request.method == 'POST':
            form = ProfileUpdate(request.POST, instance=user_obj)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(user.password)
                user.save()
                return redirect('dashboard')
    context = {
        "user": user_obj,
        "form": form
    }
    return render(request, 'profile_update.html', context)


def dashboard(request):
    if request.user.is_anonymous:
        return redirect('login')
    context = {
        "planned_events":Event.objects.filter(planner=request.user),
        "attended_events":Attendee.objects.filter(user=request.user),
    }
    return render(request,'dashboard.html',context)

def event_details(request,event_id):
    if request.user.is_anonymous:
        return redirect('login')
    event_obj = Event.objects.get(id=event_id)
    user_obj = event_obj.planner
    if request.user != user_obj:
        messages.error(request, "You have no access.")
        return redirect('home')
    else:
        context = {
            "event": event_obj
        }
    return render(request,'event_details.html',context)

def event_update(request,event_id):
    if request.user.is_anonymous:
        return redirect('login')
    event_obj = Event.objects.get(id=event_id)
    user_obj = event_obj.planner
    if request.user != user_obj:
        messages.error(request, "You have no access.")
    else:
        form = EventForm(instance=event_obj)
        if request.method == "POST":
            form = EventForm(request.POST, instance=event_obj)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.available_tickets = obj.tickets - obj.booked_tickets
                obj.save()
                return redirect('event-details',event_id)
        context = {
            "event": event_obj,
            "form": form,
        }
        return render(request, 'event_update.html', context)

def events_list(request):
    if request.user.is_anonymous:
        return redirect('login')
    queryset_list = Event.objects.filter(date__gte=datetime.today()).order_by('-available_tickets')
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(planner__username__icontains=query)
            ).distinct()
    context = {
        "events": queryset_list
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
            obj.available_tickets = obj.tickets - obj.booked_tickets
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
            if event_obj.available_tickets >= obj.reserved_tickets:
                obj.event = event_obj
                obj.user = request.user
                event_obj.available_tickets -= obj.reserved_tickets
                event_obj.booked_tickets += obj.reserved_tickets
                event_obj.save()
                obj.save()
                return redirect('dashboard')
            else:
                messages.error(request, "Event is fully booked.")
                return redirect('events-list')
    context = {
        "event": event_obj,
        "form": form
    }
    return render(request, 'book_event.html', context)
