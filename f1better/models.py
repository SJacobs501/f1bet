from django.db import models
from django.contrib.auth.models import User

class Track(models.Model):
    name = models.CharField(max_length=250)
    image = models.CharField(max_length=1000, default='https://i.imgur.com/xrM0pYH.png')

    def __str__(self):
        return '{}'.format(self.name)

class Driver(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

class Race(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    event = models.CharField(max_length=250)
    multiplier = models.DecimalField(decimal_places=1, max_digits=6)
    end_date = models.DateField()
    winner = models.ForeignKey(Driver, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.winner is None:
            activity = "ACTIVE"
        else:
            activity = "ENDED"
        return '{} {}, Date: {}, Multiplier {}, {}'.format(self.track, self.event, self.end_date, self.multiplier, activity)

# Matches races and drivers
class RaceDriver(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.race, self.driver)

class Bet(models.Model):
    money = models.DecimalField(decimal_places=2, max_digits=8)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def reward(self):
        return self.race.multiplier * self.money

    def is_win(self):
        return self.race.winner == self.driver

    def __str__(self):
        return '{} bet ${} on {}'.format(self.user, self.money, self.driver)

    def my_bets(self):
        return '{} dollar on {} ({}, {})'.format(self.money, self.driver, self.race.track, self.race.event)

class UserBalance(models.Model):
    balance = models.DecimalField(decimal_places=2, max_digits=8)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
