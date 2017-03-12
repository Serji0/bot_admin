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
        dictionary = {
            'events': events,
            'football': ['EPL', 'Bundesliga', 'LaLiga', 'Serie_A', 'Ligue_1', 'RFPL', 'Champions_league',
                         'Europa_league', 'Ukraine_league', 'FNL', 'other'],
            'basketball': ['NBA', 'other'],
            'hockey': ['NHL', 'KHL', 'other'],
            'tennis': ['ATP', 'WTA', 'other'],
            'cybersport': ['CS GO', 'Dota 2', 'League of legends', 'FIFA', 'Starcraft', 'other'],
            'other': ['other'],
            'EPL': ['Arsenal', 'Aston Villa', 'Bournemouth', 'Burnley', 'Chelsea', 'Crystal Palace', 'Everton',
                    'Hull City', 'Leister City', 'Liverpool', 'Manchester City', 'Manchester United', 'Middlesbrough',
                    'Southampton', 'Stoke City', 'Sunderland', 'Swansey', 'Tottenham', 'Watford', 'West Bromwich',
                    'West Ham'],
            'Bundesliga': ['Augsburg', 'Bayer 04', 'Bayern', 'Borussia D.', 'Borussia M.', 'Darmstadt 98', 'Eintracht',
                           'Freiburg', 'Hamburger SV', 'Herta', 'Hoffenheim 1899', 'Ingolstadt 04', 'Koln', 'Mainz 05',
                           'RB Leipzig', 'Shalke 04', 'Wolfsburg', 'Werder'],
            'LaLiga': ['Alaves', 'Athletic', 'Atletico', 'Celta', 'Deportivo', 'Eibar', 'Espanyol', 'FC Barcelona',
                       'Granada', 'Las Palmas', 'Leganes', 'Malaga', 'Osasuna', 'R. Betis', 'R. Madrid', 'R. Sociedad',
                       'Sevilla', 'Sporting', 'Valencia', 'Villareal'],
            'Serie_A': ['Atalanta', 'Bologna', 'Cagliari', 'Chievoverona', 'Crotone', 'Empoli', 'Fiorentina', 'Genoa',
                        'Inter', 'Juventus', 'Lazio', 'Milan', 'Napoli', 'Palermo', 'Pescara', 'Roma', 'Sampdoria',
                        'Sassuolo', 'Torino', 'Udinese'],
            'Ligue_1': ['Angers', 'Bastia', 'Bordeaux', 'Caen', 'Dijon', 'Guingamp', 'LOSC', 'Lorient', 'OL', 'OM',
                        'Metz', 'Monaco', 'Monpellier', 'Nancy', 'Nantes', 'Nice', 'PSG', 'Rennais', 'Saint-Etienne',
                        'Toulouse'],
            'RFPL': ['Amkar', 'Anji', 'Arsenal', 'CSKA', 'Krasnodar', 'Krylia sovetov', 'Lokomotiv', 'Orenburg',
                     'Rostov', 'Rubin', 'Spartak', 'Terek', 'Tom', 'UFA', 'Ural', 'Zenit'],
            'Ukraine_league': ['Chornomorets', 'Dnipro', 'Dynamo', 'Karpaty', 'Oleksandria', 'Olimpick', 'Shaktar',
                               '	Stal Kamianske', 'Volyn', 'Vorskla', 'Zirka', 'Zorya'],
            'FNL': ['Baltika', 'Dynamo', 'Enisey', 'Fakel', 'Himki', 'Kuban', 'Luch-energia', 'Mordovia', 'Neftehimik',
                    'Shinnik', 'Sibir', 'SKA', 'Sokol', 'Spartak-2', 'Spartak-Nalchik', 'Tambov', 'Tosno', 'Tumen',
                    'Volgar', 'Zenit-2'],
            'Champions_league': [],
            'Europa_league': ['Ajax', 'Anderlecht', 'APOEL', 'Besiktas', 'Borussia M.', 'Celta', 'Genk', 'Gent',
                              'Kobenhagen', 'Krasnodar', 'Lyon', 'Manchester United', 'Olimpiakos', 'Roma', 'Rostov',
                              'Shalke 04'],
            'NBA': ['Atlanta', 'Boston', 'Brooklyn', 'Charlotte', 'Chicago', 'Cleveland', 'Dallas', 'Denver', 'Detroit',
                    'Golden State', 'Houston', 'Indiana', 'LA Clippers', 'LA Lakers', 'Miami', 'Milwaukee', 'Minnesota',
                    'New Orleans', 'New York', 'Okhlahoma', 'Orlando', 'Philadelphia', 'Phoenix', 'Portland',
                    'Sacramento', 'San Antonio', 'Toronto', 'Utah', 'Washington'],
            'NHL': [],
            'KHL': []
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



