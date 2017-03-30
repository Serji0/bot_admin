from django.db import models
from datetime import datetime


class User(models.Model):
    def __str__(self):
        return self.qiwi

    telegram_id = models.CharField(max_length=15, default='', unique=True)
    balance = models.FloatField(default=0)
    qiwi = models.CharField(max_length=20, default='', unique=True)


class Event(models.Model):
    def __str__(self):
        return str(self.team1 + ' - ' + self.team2)

    sport = models.CharField(max_length=20, default='football')
    league = models.CharField(max_length=25, default='EPL')
    team1 = models.CharField(max_length=25, default='')
    team2 = models.CharField(max_length=25, default='')
    time = models.DateTimeField(default=datetime.now())
    win_ratio = models.FloatField(default=1)
    draw_ratio = models.FloatField(default=1)
    lose_ratio = models.FloatField(default=1)
    total_value = models.FloatField(default=2.5)
    over_ratio = models.FloatField(default=1)
    under_ratio = models.FloatField(default=1)
    handicap1 = models.FloatField(default=0)
    handicap2 = models.FloatField(default=0)
    handicap1_ratio = models.FloatField(default=1)
    handicap2_ratio = models.FloatField(default=1)
    total1 = models.CharField(max_length=3, default='--')
    total2 = models.CharField(max_length=3, default='--')
    max_bet = models.IntegerField(default=1000)
    status = models.CharField(max_length=10, default='active')


class Bet(models.Model):
    def __str__(self):
        return str(str(self.event) + ' ' + str(self.choice) + ' ' + str(self.user))

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.CharField(max_length=15, default='')
    ratio = models.FloatField(default=1)
    amount = models.FloatField(default=0)
    status = models.CharField(max_length=10, default='unknown')


class Team(models.Model):
    def __str__(self):
        return str(self.name)

    sport = models.CharField(max_length=20, default='')
    league = models.CharField(max_length=25, default='')
    name = models.CharField(max_length=25, default='')

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default='new')
    type = models.CharField(max_length=30, default='unknown')
    comment = models.CharField(max_length=200, default='')