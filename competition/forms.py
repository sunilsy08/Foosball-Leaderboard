from django import forms

from .models import Team, Match


class CreateTeamForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = ['player1','player2']



class CreateMatchForm(forms.ModelForm):
	class Meta:
		model = Match
		fields = ['team1','team2','team1_score','team2_score']

		

