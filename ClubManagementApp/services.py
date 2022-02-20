import random
from random import randint
from .models import TeamDetails,VenueDetails
from django.core.mail import send_mail
from django.conf import settings

def GetTeamID():
    team_id = randint(1000,9999)
    
    exist=TeamDetails.objects.filter(team_user_id=team_id)
    if exist:
        GetTeamID()
    return team_id

def GetvenueID():
    venue_id=randint(10000,99999)
    exist=VenueDetails.objects.filter(venue_user_id=venue_id)
    if exist:
        GetvenueID()
    return venue_id

def email_team(mail_recipient,user_name,passwd):
    subject="username and password"
    message="Hi your username is "+user_name+" and temporary password is "+passwd
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[mail_recipient,]
    send_mail(subject,message,email_from,recipient_list)

def email_player(mail_recipient,user_name,passwd):
    subject="username and password"
    message="Hi your username is "+user_name+" and temporary password is "+passwd
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[mail_recipient,]
    send_mail(subject,message,email_from,recipient_list)

def account_status(mail_recipient,status):
    subject="Account Status"
    message="Hi Your Account Has Been "+status+" By The Admin.",
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[mail_recipient,]
    send_mail(subject,message,email_from,recipient_list)