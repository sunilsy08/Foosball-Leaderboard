from django.shortcuts import render, redirect
from django.http import request, HttpResponse
from django.views.generic import CreateView
from django.db.models import Q
from django.urls import reverse_lazy, reverse

from .models import Team, Match
from .forms import CreateTeamForm, CreateMatchForm


class createTeamView(CreateView):
    template_name = "team/form.html"
    form_class = CreateTeamForm

    def get_success_url(self):
        return reverse('team-detail', kwargs={'pk': self.object.id})


class createMatchView(CreateView):
    template_name = "match/form.html"
    form_class = CreateMatchForm
    success_url = reverse_lazy("home")


def getTeam(team):
    p1 = team.player1
    p2 = team.player2
    tm = Team.objects.filter(Q(player1=p1) & Q(player2=p2))
    return tm


def createMatch(request):
    if request.method == 'POST':
        form = CreateMatchForm(request.POST)
        if form.is_valid():
            match = Match()
            match.team1 = form.cleaned_data.get('team1')
            match.team2 = form.cleaned_data.get('team2')
            match.team1_score = form.cleaned_data.get('team1_score')
            match.team2_score = form.cleaned_data.get('team2_score')
            match.save()

            if match.team1_score > match.team2_score:
                match.team1.foosball_points += 3
                match.team2.foosball_points -= 1
            elif match.team1_score < match.team2_score:
                match.team2.foosball_points += 3
                match.team1.foosball_points -= 1
            match.team1.save()
            match.team2.save()
            return redirect("leaderboard")
    else:
        form = CreateMatchForm()
    return render(request, 'match/form.html', {'form': form})


def teamDetail(request, pk):
    team = Team.objects.get(pk=pk)
    matches = Match.objects.filter(Q(team1=team) | Q(team2=team))
    content = {
        'team': team,
        'matches': matches
    }
    return render(request, 'team/detail.html', {'content': content})


def showLeaderboard(request):

	teams = Team.objects.all().order_by('-foosball_points')
	counter = 1
	till = teams[0].foosball_points
	final = []
	for team in teams:
		if team.foosball_points < till:
			counter = counter+1
			till = team.foosball_points
		if counter == 4:
			break
		final.append(team)

	return render(request, 'leaderboard.html', {'teams': final})


def home(request):
    return render(request, 'home.html', {})
