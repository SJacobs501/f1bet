from django.contrib import admin
from .models import Track, Driver, Race, RaceDriver, Bet

admin.site.register(Race)
admin.site.register(Track)
admin.site.register(Driver)
admin.site.register(RaceDriver)
admin.site.register(Bet)