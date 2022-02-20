from django import forms
from ..models import TeamDetails,PlayerDetails
import re


class TeamRegForm(forms.ModelForm):
    team_name=forms.CharField(label="Team Name",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    team_place=forms.CharField(label="Place",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    team_phno=forms.CharField(label="Contact No.",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    team_email=forms.CharField(label="Email",widget=forms.EmailInput(attrs={'style':'width:300px','class':'form-control'}))
    team_logo=forms.ImageField(label="Team Logo",widget=forms.FileInput(attrs={'style':'width:300px','class':'form-control'}))
    class Meta:
        model=TeamDetails
        fields=('team_name','team_place','team_phno','team_logo','team_email')



class AddPlayerForm(forms.ModelForm):
    player_name=forms.CharField(label="Player Name",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    player_address=forms.CharField(label="Address",widget=forms.Textarea(attrs={'style':'width:300px','class':'form-control'}))
    player_dob=forms.CharField(label="D.O.B",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    player_email=forms.CharField(label="Email",widget=forms.EmailInput(attrs={'style':'width:300px','class':'form-control'}))
    player_img=forms.ImageField(label="Upload Pic",widget=forms.FileInput(attrs={'style':'width:300px','class':'form-control'}))
    player_height=forms.CharField(label="Height",widget=forms.NumberInput(attrs={'style':'width:300px','class':'form-control'}))
    player_weight=forms.CharField(label="Weight",widget=forms.NumberInput(attrs={'style':'width:300px','class':'form-control'}))
    player_ph=forms.CharField(label="Contact No.",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    class Meta:
        model=PlayerDetails
        fields=('player_name','player_address','player_dob','player_email','player_img','player_height','player_weight','player_ph')