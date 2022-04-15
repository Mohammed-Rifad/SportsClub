from django import forms
from django.db.models import fields
from ..models import *
import re



class LoginForm(forms.Form):
    login_id=forms.CharField(label="User Name",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    login_passwd=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'style':'width:300px','class':'form-control'}))



class AddSportForm(forms.ModelForm):
    
    sport_name=forms.CharField(label="Sport Name",widget=forms.TextInput(attrs={'style':'width:200px','class':'form-control'}))
    
    class Meta:
        model=SportsDetail
        fields=('sport_name','sport_type')

    def clean_sport_name(self):
        sport_name=self.cleaned_data['sport_name']
        if not re.match('^[A-Z a-z ]+$',sport_name):
            raise forms.ValidationError("Name Should Be Of Letters Only")
        return sport_name



class AdminNotificationform(forms.ModelForm):
    notfn_content=forms.CharField(label="Notification",widget=forms.Textarea(attrs={'rows':'5','cols':'25',}))
    notfn_title=forms.CharField(label="Tite",widget=forms.TextInput())
    class Meta:
        model=AdminNotification
        fields=('notfn_title','notfn_content',)

class TournamentForm(forms.ModelForm):
    tournament_title=forms.CharField(label="Tournament Title",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    players_allowed=forms.CharField(label=" Max Players Allowed",widget=forms.NumberInput(attrs={'style':'width:300px','class':'form-control'}))
    start_date=forms.CharField(label="Start Date",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    end_date=forms.CharField(label="End Date",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    reg_date=forms.CharField(label="Last Date For Registration",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    reg_fee=forms.CharField(label="Registration Fee",widget=forms.NumberInput(attrs={'style':'width:300px','class':'form-control'}))
    win_prize=forms.CharField(label="Prize Money",widget=forms.NumberInput(attrs={'style':'width:300px','class':'form-control'}))
    
    class Meta:
        model=TournamentDetails
        fields=('tournament_title','players_allowed','start_date','end_date','reg_date','reg_fee','win_prize')
    