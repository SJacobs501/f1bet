from django.db import models
from django.contrib.auth.models import User

class Track(models.Model):
    name = models.CharField(max_length=250)
    event = models.CharField(max_length=250)
    image = models.CharField(max_length=1000)

    def __str__(self):
        return '{} {}'.format(self.name, self.event)

class Driver(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

# Matches tracks and drivers
class TrackDriver(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.track, self.driver)

class Bet(models.Model):
    # is a bet finished? (meaning we know the result)
    finished = models.BooleanField(default=False)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)