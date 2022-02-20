from django import forms
from ..models import VenueDetails,BlockDetails
import re

class VenueRegForm(forms.ModelForm):
    venue_choices=(
        ('football','Football'),
        ('cricket','Cricket'),
        ('both','Both')
    )
    venue_name=forms.CharField(label="Venue Name",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    venue_type=forms.CharField(label="Venue Type",widget=forms.Select(choices=venue_choices, attrs={'style':'width:300px','class':'form-control'}))
    venue_address=forms.CharField(label="Address",widget=forms.Textarea(attrs={'style':'width:300px','class':'form-control'}))
    venue_contact=forms.CharField(label="Contact",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    venue_email=forms.CharField(label="Email",widget=forms.EmailInput(attrs={'style':'width:300px','class':'form-control'}))
    venue_pic=forms.ImageField(label="Upload Pic",widget=forms.FileInput(attrs={'style':'width:300px','class':'form-control'}))
    venue_seat=forms.ImageField(label="Block Pic",widget=forms.FileInput(attrs={'style':'width:300px','class':'form-control'}))
    
    class Meta:
        model=VenueDetails
        fields=('venue_name','venue_type','venue_address','venue_contact','venue_email','venue_pic','venue_seat')

class BlockForm(forms.ModelForm):
    block_title=forms.CharField(label="Block Name",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    amount=forms.CharField(label="Amount",widget=forms.NumberInput(attrs={'style':'width:300px','class':'form-control'}))
    total_seats=forms.CharField(label="Seats Available",widget=forms.NumberInput(attrs={'style':'width:300px','class':'form-control'}))
    class Meta:
        model=BlockDetails
        exclude=('venue_id',)