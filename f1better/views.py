from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from .forms import AddDriverForm, AddTrackForm

# Create your views here.
def races(request):
    tracks = Track.objects.all()
    context = {'tracks': tracks}
    return render(request, "races.html", context)

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
        return redirect('login')
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
            return redirect('races')
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
                return redirect('races')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    django_logout(request)
    return redirect('races')

def help(request):
    return render(request, 'help.html')

def about_us(request):
    return render(request, 'about_us.html')

def manage(request):
    user = request.user
    if not request.user.is_authenticated:
        return redirect('login')
    if not user.is_staff:
        return redirect('races')

    races = TrackDriver.objects.all()
    tracks = Track.objects.all()
    drivers = Driver.objects.all()
    form_add_driver = AddDriverForm()
    form_add_track = AddTrackForm()
    context = {
        'races': races,
        'tracks': tracks,
        'drivers': drivers,
        'form_add_driver': form_add_driver,
        'form_add_track': form_add_track,
    }
    return render(request, 'manage.html', context)

def add_race(request):
    user = request.user
    if not request.user.is_authenticated:
        return redirect('login')
    if not user.is_staff:
        return redirect('races')

    if request.method == 'POST':
        track_id = request.POST.get("track")
        track = Track.objects.get(id=track_id)
        driver_ids = request.POST.getlist('drivers')

        for driver_id in driver_ids:
            driver = Driver.objects.get(id=driver_id)
            trackDriver = TrackDriver(track=track, driver=driver)
            trackDriver.save()

    return redirect('manage')

def add_driver(request):
    user = request.user
    if not request.user.is_authenticated:
        return redirect('login')
    if not user.is_staff:
        return redirect('races')

    if request.method == 'POST':
        form = AddDriverForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            driver = Driver(first_name=first_name, last_name=last_name)
            driver.save()

    return redirect('manage')

def add_track(request):
    user = request.user
    if not request.user.is_authenticated:
        return redirect('login')
    if not user.is_staff:
        return redirect('races')

    if request.method == 'POST':
        form = AddTrackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            event = form.cleaned_data['event']
            image = form.cleaned_data['image']

            track = Track(name=name, event=event, image=image)
            track.save()
    return redirect('manage')

def remove_driver(request):
    user = request.user
    if not request.user.is_authenticated:
        return redirect('login')
    if not user.is_staff:
        return redirect('races')

    if request.method == 'POST':
        driver_id = request.POST.get("driver_to_remove")
        if driver_id is None:
            return redirect('manage')
        driver = Driver.objects.get(id=driver_id)
        driver.delete()
    return redirect('manage')

def remove_track(request):
    user = request.user
    if not request.user.is_authenticated:
        return redirect('login')
    if not user.is_staff:
        return redirect('races')

    if request.method == 'POST':
        track_id = request.POST.get("track_to_remove")
        if track_id is None:
            return redirect('manage')
        track = Track.objects.get(id=track_id)
        track.delete()
    return redirect('manage')
