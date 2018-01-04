from django.http import Http404, HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from django.core.validators import ValidationError
from django.contrib.auth.models import User
from .forms import BetForm

# Create your views here.
def index(request):
    tracks = Track.objects.all()
    context = {'tracks': tracks}
    return render(request, "index.html", context)

def details_track(request, track_id):
    track = Track.objects.get(id=track_id)

    # Select driver_ids from track_drivers by track id.
    track_drivers = TrackDriver.objects.filter(track_id=track.id).values('driver')

    # Get the drivers for this track.
    drivers = Driver.objects.filter(id__in=[track_drivers])

    bets = Bet.objects.filter(track=track_id)

    context = {
        'track': track,
        'drivers': drivers,
        'bets': bets
    }
    return render(request, "details_track.html", context)

def make_bet(request, track_id):
    # if not logged in, go to login page.
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        if request.method == 'POST':
            track = Track.objects.get(id=track_id)

            try:
                money = request.POST['money']
                driver_id = request.POST['driver']
                driver = Driver.objects.get(id=driver_id)
                user = request.user
            except:
                return redirect('details_track', track_id=track_id)

            # check if user exists
            if user is None:
                return render(request, 'details_track.html')

            bet = Bet(money=money, track=track, driver=driver, user=user)
            bet.save()

        return redirect('details_track', track_id=track_id)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    django_logout(request)
    return redirect('index')