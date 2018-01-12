from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from .forms import AddDriverForm, AddTrackForm
from collections import defaultdict

# Create your views here.
def races(request):
    races = Race.objects.all()
    context = {'races': races}
    return render(request, "races.html", context)

def details_track(request, race_id):
    race = Race.objects.get(id=race_id)

    # Select driver_ids from track_drivers by track id.
    race_drivers = RaceDriver.objects.filter(race=race).values('driver')

    # Get the drivers for this track.
    drivers = Driver.objects.filter(id__in=[race_drivers])

    bets = Bet.objects.filter(race=race_id)

    balance = get_balance(request.user)

    bet_error_message = request.session.get('bet_error_message')
    if bet_error_message:
        del request.session['bet_error_message']

    context = {
        'race': race,
        'drivers': drivers,
        'bets': bets,
        'balance': balance,
        'bet_error_message': bet_error_message
    }
    return render(request, "details_track.html", context)

# get balance of user
def get_balance(user):
    try:
        balance = UserBalance.objects.get(user=user)
    except UserBalance.DoesNotExist:
        balance = 0
    return balance

def make_bet(request, race_id):
    # if not logged in, go to login page.
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            race = Race.objects.get(id=race_id)

            try:
                money = request.POST['money']
                driver_id = request.POST['driver']
                driver = Driver.objects.get(id=driver_id)
                user = request.user
            except:
                request.session['bet_error_message'] = "Please select a driver to vote on."
                return redirect('details_track', race_id=race_id)

            try:
                money_int = float(money)
            except ValueError:
                request.session['bet_error_message'] = "You did not enter a valid number!"
                return redirect('details_track', race_id=race_id)

            # check if user exists
            if user is None:
                return redirect('details_track', race_id=race_id)

            #check if balance
            balance = get_balance(user)
            if money_int > balance:
                request.session['bet_error_message'] = "You do not have enough balance."
                return redirect('details_track', race_id=race_id)

            elif money_int == 0:
                request.session['bet_error_message'] = "You cannot bet 0$."
                return redirect('details_track', race_id=race_id)

            bet = Bet(money=money, race=race, driver=driver, user=user)
            bet.save()

        return redirect('details_track', race_id=race_id)

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

    add_race_error_message = request.session.get('add_race_error_message')
    if add_race_error_message:
        del request.session['add_race_error_message']

    add_track_error_message = request.session.get('add_track_error_message')
    if add_track_error_message:
        del request.session['add_track_error_message']

    remove_race_error_message = request.session.get('remove_race_error_message')
    if remove_race_error_message:
        del request.session['remove_race_error_message']

    remove_driver_error_message = request.session.get('remove_driver_error_message')
    if remove_driver_error_message:
        del request.session['remove_driver_error_message']

    remove_track_error_message = request.session.get('remove_track_error_message')
    if remove_track_error_message:
        del request.session['remove_track_error_message']

    races = Race.objects.all()
    tracks = Track.objects.all()
    drivers = Driver.objects.all()
    form_add_driver = AddDriverForm()
    form_add_track = AddTrackForm()
    context = {
        'add_race_error_message': add_race_error_message,
        'add_track_error_message': add_track_error_message,
        'remove_race_error_message': remove_race_error_message,
        'remove_driver_error_message': remove_driver_error_message,
        'remove_track_error_message': remove_track_error_message,
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
        event = request.POST.get("event")
        multiplier = request.POST.get("multiplier")

        if track_id == '0':
            request.session['add_race_error_message'] = "You did not choose a track!"
            return redirect('manage')

        if not event:
            request.session['add_race_error_message'] = "Please enter the name of the event."
            return redirect('manage')

        # check if there's already a race with this track.
        races = Race.objects.filter(track_id=track_id)
        if races.count() > 0:
            request.session['add_race_error_message'] = "There's already a race going on for this track!"
            return redirect('manage')

        track = Track.objects.get(id=track_id)
        driver_ids = request.POST.getlist('drivers')

        if len(driver_ids) < 2:
            request.session['add_race_error_message'] = "You need atleast 2 drivers for a race."
            return redirect('manage')

        race = Race(track=track, event=event, multiplier=multiplier)
        race.save()

        for driver_id in driver_ids:
            driver = Driver.objects.get(id=driver_id)
            race_driver = RaceDriver(race=race, driver=driver)
            race_driver.save()
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

            if Track.objects.filter(name=name):
                request.session['add_track_error_message'] = "A track with this name already exists!"
                return redirect('manage')

            image = form.cleaned_data['image']
            
            track = Track(name=name)
            if image:
                track.image=image
            track.save()
    return redirect('manage')

def remove_race(request):
    user = request.user
    if not request.user.is_authenticated:
        return redirect('login')
    if not user.is_staff:
        return redirect('races')

    if request.method == 'POST':
        race_id = request.POST.get("race_to_remove")
        if race_id is None:
            request.session['remove_race_error_message'] = "Please choose a race."
            return redirect('manage')

        race = Race.objects.get(id=race_id)
        race.delete()

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
            request.session['remove_driver_error_message'] = "Please choose a driver."
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
            request.session['remove_track_error_message'] = "Please choose a track."
            return redirect('manage')
        track = Track.objects.get(id=track_id)
        track.delete()
    return redirect('manage')
