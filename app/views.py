from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from app.models import *
from app.forms import *


@login_required(login_url='/authorization/')
def main(request):
    return render(request, 'index.html')


def authorization(request):
    if request.method == 'POST':
        form = AuthorizationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data.get('username'), password=data.get('password'))
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
    else:
        form = AuthorizationForm()
    return render(request, 'authorization.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/authorization')


class UsersView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'users.html', {'users': users})


class UserView(View):
    def get(self, request, id):
        user = User.objects.filter(id=id)[0]
        bets = Bet.objects.filter(user=user)
        dictionary = {
            'user': user,
            'bets': bets
        }
        return render(request, 'user.html', dictionary)


def edit_user(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        user = User.objects.filter(id=id)[0]
        user.qiwi = request.POST.get('qiwi')
        user.balance = request.POST.get('balance')
        user.save()
        return HttpResponseRedirect('/users/')
    return HttpResponseRedirect('/')


class RequestsView(View):
    def get(self, request):
        requests = Request.objects.all()
        return render(request, 'requests.html', {'requests': requests})


class EventsView(View):
    def get(self, request):
        events = Event.objects.all()
        teams = Team.objects.all()
        Laliga = []
        Bundesliga = []
        EPL = []
        RFPL = []
        FNL = []
        Ligue_1 = []
        Serie_A = []
        Champions_league = []
        Europa_league = []
        Ukraine_league = []
        NBA = []
        NHL = []
        KHL = []

        for team in teams:
            if team.league == 'EPL':
                EPL.append(team.name)
            if team.league == 'LaLiga':
                Laliga.append(team.name)
            if team.league == 'Serie_A':
                Serie_A.append(team.name)
            if team.league == 'Bundesliga':
                Bundesliga.append(team.name)
            if team.league == 'Ligue_1':
                Ligue_1.append(team.name)
            if team.league == 'RFPL':
                RFPL.append(team.name)
            if team.league == 'FNL':
                FNL.append(team.name)
            if team.league == 'Ukraine_league':
                Ukraine_league.append(team.name)
            if team.league == 'Champions_league':
                Champions_league.append(team.name)
            if team.league == 'Europa_league':
                Europa_league.append(team.name)
            if team.league == 'NBA':
                NBA.append(team.name)
            if team.league == 'NHL':
                NHL.append(team.name)
            if team.league == 'KHL':
                KHL.append(team.name)

        dictionary = {
            'events': events,
            'football': ['EPL', 'Bundesliga', 'LaLiga', 'Serie_A', 'Ligue_1', 'RFPL', 'Champions_league',
                         'Europa_league', 'Ukraine_league', 'FNL', 'other'],
            'basketball': ['NBA', 'other'],
            'hockey': ['NHL', 'KHL', 'other'],
            'tennis': ['ATP', 'WTA', 'other'],
            'cybersport': ['CS GO', 'Dota 2', 'League of legends', 'FIFA', 'Starcraft', 'other'],
            'other': ['other'],
            'EPL': EPL,
            'Bundesliga': Bundesliga,
            'LaLiga': Laliga,
            'Serie_A': Serie_A,
            'Ligue_1': Ligue_1,
            'RFPL': RFPL,
            'Ukraine_league': Ukraine_league,
            'FNL': FNL,
            'Champions_league': Champions_league,
            'Europa_league': Europa_league,
            'NBA': NBA,
            'NHL': NHL,
            'KHL': KHL
        }
        return render(request, 'events.html', dictionary)


def add_event(request):
    if request.method == 'POST':
        event = Event()
        event.sport = request.POST.get('sport')
        event.league = request.POST.get('league')
        event.team1 = request.POST.get('team1')
        event.team2 = request.POST.get('team2')
        event.time = request.POST.get('time')
        event.win_ratio = request.POST.get('win_ratio')
        event.draw_ratio = request.POST.get('draw_ratio')
        event.lose_ratio = request.POST.get('lose_ratio')
        event.total_value = request.POST.get('total_value')
        event.under_ratio = request.POST.get('under_ratio')
        event.over_ratio = request.POST.get('over_ratio')
        event.max_bet = request.POST.get('max_bet')
        event.save()
        return HttpResponseRedirect('/events')
    return HttpResponseRedirect('/')


class EventView(View):
    def get(self, request, id):
        event = Event.objects.filter(id=id)[0]
        bets = Bet.objects.filter(event=event)
        dictionary = {
            'event': event,
            'bets': bets
        }
        return render(request, 'event.html', dictionary)


def edit_event(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        event = Event.objects.filter(id=id)[0]
        event.win_ratio = request.POST.get('win_ratio')
        event.draw_ratio = request.POST.get('draw_ratio')
        event.lose_ratio = request.POST.get('lose_ratio')
        event.total_value = request.POST.get('total_value')
        event.under_ratio = request.POST.get('under_ratio')
        event.over_ratio = request.POST.get('over_ratio')
        event.save()
        return HttpResponseRedirect('/events/')
    return HttpResponseRedirect('/')


def set_score(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        event = Event.objects.filter(id=id)[0]
        event.total1 = request.POST.get('total1')
        event.total2 = request.POST.get('total2')
        event.save()
        bets = Bet.objects.filter(event_id=id).all()
        for bet in bets:
            u_id = bet.user_id
            user = User.objects.filter(id=u_id)[0]
            if bet.choice == 'win1':
                if event.total1 > event.total2:
                    bet.status = '+++'
                    user.balance += bet.ratio * bet.amount
                else:
                    bet.status = '-----'
            elif bet.choice == 'draw':
                if event.total1 == event.total2:
                    bet.status = '+++'
                    user.balance += bet.ratio * bet.amount
                else:
                    bet.status = '-----'
            elif bet.choice == 'win2':
                if event.total2 > event.total1:
                    bet.status = '+++'
                    user.balance += bet.ratio * bet.amount
                else:
                    bet.status = '-----'
            elif bet.choice == 'under':
                if (event.total1 + event.total2) < event.total_value:
                    bet.status = '+++'
                    user.balance += bet.ratio * bet.amount
                else:
                    bet.status = '-----'
            elif bet.choice == 'over':
                if (event.total1 + event.total2) > event.total_value:
                    bet.status = '+++'
                    user.balance += bet.ratio * bet.amount
                else:
                    bet.status = '-----'
            user.save()
            bet.save()
        return HttpResponseRedirect('/events')
    return HttpResponseRedirect('/')


def delete_event(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        event = Event.objects.filter(id=id)[0]
        event.delete()
        return HttpResponseRedirect('/events')
    return HttpResponseRedirect('/')

def close_event(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        event = Event.objects.filter(id=id)[0]
        event.status = 'closed'
        event.save()
        return HttpResponseRedirect('/events')
    return HttpResponseRedirect('/')



