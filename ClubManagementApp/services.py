import random
from random import randint
from traceback import print_tb
from datetime import datetime
from ClubManagementApp.views.TeamView import TournamentDetail
from .models import Fixture, TeamDetails, TournamentDetails,VenueDetails
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

def FixtureGenerate(model_data,count):
    team1=[]
    team2=[]
    team1_id=[]
    team2_id=[]
    fixture1=[]
    fixture2=[]
    fixture3=[]
    c=0
    fxt_dict1={}
    fxt_dict2={}
    fxt_dict3={} 
    fxt_arr1=[]
    final_fixt={} 
    if count % 2 == 0:
         
        for i in model_data:
            if c<count/2:
                team1.append(i.team_id.team_name.lower())
                team1_id.append(i.team_id)
                c+=1
            else:
                team2.append(i.team_id.team_name.lower())
                team2_id.append(i.team_id)
    print(team1)
    print(team2)
    for i in range(len(team1)):
        for j in range(i+1,len(team1)):
            match=team1[i]+' vs ' + team1[j]

            t1=TeamDetails.objects.get(team_name=team1[i]) 
            t2=TeamDetails.objects.get(team_name=team1[j]) 

            fxt_dict1['team1']=t1.team_name
            fxt_dict1['team2']=t2.team_name
            fxt_dict1['t1']=t1 
            fxt_dict1['t2']=t2
            fxt_dict1['match']=match
            fxt_arr1.append(fxt_dict1)
            fxt_dict1={}
            fixture1.append(match)

   
    for i in range(len(team2)):
        for j in range(i+1,len(team2)):
            match=team2[i]+' vs ' + team2[j]
            
            fixture2.append(match)
    
            t1=TeamDetails.objects.get(team_name=team2[i]) 
            t2=TeamDetails.objects.get(team_name=team2[j]) 
            fxt_dict1['team1']=t1.team_name
            fxt_dict1['team2']=t2.team_name
            fxt_dict1['t1']=t1 
            fxt_dict1['t2']=t2 
            fxt_dict1['match']=match
            fxt_arr1.append(fxt_dict1)
            fxt_dict1={}

    for i in range(len(team2)):
        for j in range(len(team1)):
            match=team1[i]+' vs ' + team2[j]
            fixture3.append(match)
            t1=TeamDetails.objects.get(team_name=team1[i]) 
            t2=TeamDetails.objects.get(team_name=team2[j]) 

            fxt_dict1['team1']=t1.team_name
            fxt_dict1['team2']=t2.team_name
            fxt_dict1['t1']=t1 
            fxt_dict1['t2']=t2 
            fxt_dict1['match']=match
            fxt_arr1.append(fxt_dict1)
            fxt_dict1={}
    
    # print('******************************************')
    # print(fxt_arr1,'jceduedy')

    # print(len(fxt_arr1))
    # for i in fxt_arr1:
    #     f=Fixture()

    # final_fixture=fixture1+fixture2+fixture3

     
    return fxt_arr1