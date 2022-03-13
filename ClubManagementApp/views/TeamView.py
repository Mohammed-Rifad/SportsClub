from ClubManagementApp.Forms.TeamForm import AddPlayerForm
from django.shortcuts import render,redirect
from django.http import HttpResponse
from ..models import PlayerDetails,SportsDetail, TeamDetails, TournamentDetails, TournamentPlayers, TournamentRegistration
from ..Forms import TeamForm
from passlib.hash import pbkdf2_sha256
from django.utils.crypto import get_random_string
from ..services import email_player, email_team

def TeamHome(request):
    # print(request.session['team_id'])
    # data=SportsDetail.objects.get(sport_id=request.session['team_type'])
    # print(data.sport_name)
    return render(request,'TeamAdmin/TeamHome.html')


def AddPlayer(request):
   
    # player=PlayerDetails.objects.get(player_id=1)
    # print(player.player_img.url)
    form=AddPlayerForm()
    data=SportsDetail.objects.get(sport_id=request.session['team_type'])
    sport_type=data.sport_name
    if sport_type=='cricket':
        positions=['Batsman','Bowler','Wicket Keeper','All Rounder']
    elif sport_type=="football":
        positions=['striker','mid-fielder','defender','right wing back','goal keeper']
    

    if request.method=='POST':
        print('here')
        form=AddPlayerForm(request.POST,request.FILES)
        if form.is_valid():
            team_id=TeamDetails.objects.get(team_id=request.session['team_id'])
            player_name=form.cleaned_data['player_name'].lower()
            player_address=form.cleaned_data['player_address'].lower()
            player_dob=form.cleaned_data['player_dob']
            player_email=form.cleaned_data['player_email']
            player_height=form.cleaned_data['player_height']
            player_weight=form.cleaned_data['player_weight']
            player_img=form.cleaned_data['player_img']
            player_ph=form.cleaned_data['player_ph']
            player_position=request.POST['position']
            passwd=get_random_string(length=8)
            player_passwd=pbkdf2_sha256.hash(passwd,rounds=1000,salt_size=32)
            email_exists=PlayerDetails.objects.filter(player_email=player_email).exists()
            
            if email_exists:
                msg="Email Already Exists"
                return render(request,'TeamAdmin/AddPlayer.html',{'form':form,'positions':positions,'msg':msg})
            
            phno_exists=PlayerDetails.objects.filter(player_ph=player_ph).exists()
            if phno_exists:
                msg="Phone No. Already Exists"
                return render(request,'TeamAdmin/AddPlayer.html',{'form':form,'positions':positions,'msg':msg})

            qry=PlayerDetails(team_id=team_id,player_name=player_name,player_address=player_address,player_dob=player_dob,player_email=player_email,player_ph=player_ph,player_position=player_position,player_height=player_height,player_weight=player_weight,player_img=player_img,player_passwd=player_passwd)
            qry.save()
            msg="Player Added Succesfully"
            print('passwd is',passwd)
            #email_player(player_email,player_ph,passwd)
            
            return render(request,'TeamAdmin/AddPlayer.html',{'form':form,'positions':positions,'msg':msg})
        else:
            print(form.errors)
    return render(request,'TeamAdmin/AddPlayer.html',{'form':form,'positions':positions})

def ViewPlayers(request):
    players_list=PlayerDetails.objects.filter(team_id=request.session['team_id'])
    for i in players_list:
        print(i.player_name)
    return render(request,'TeamAdmin/ViewPlayers.html',{'players_list':players_list})

def EditPlayer(request,id):
    pass

def DeletePlayer(request,id):
    player_data=PlayerDetails.objects.get(player_id=id)
    player_data.delete()
    return redirect("club_management:view_players")

def ViewPlayer(request,id):
    player_data=PlayerDetails.objects.get(player_id=id)
    return render(request,'TeamAdmin/ViewPlayerDetails.html',{'player':player_data})


def ViewTournaments(request):
    tournament_data=TournamentDetails.objects.filter(tournament_status='not completed')
    # is_registered=TournamentRegistration.objects.filter(tournament_id=)

    return render(request,'TeamAdmin/ViewTournaments.html',{'tournaments':tournament_data,})




def AddTournamentPlayers(request,id):
    tournament=TournamentDetails.objects.get(tournament_id=id)
    current_players=PlayerDetails.objects.filter(team_id=request.session['team_id'])
    added_players=TournamentPlayers.objects.filter(team_id=request.session['team_id'])
    msg=""

    current_count=TournamentPlayers.objects.filter(tournament_id=tournament.tournament_id,team_id=request.session['team_id']).count()
    approved=False
    for p in added_players:
        
        if p.player_status=='not approved' or p.player_status=='rejected':
            
            approved=True
            break;

    print(approved)
    if request.method=='POST':

        if 'checkout' in request.POST:
            pass

        if 'del' in request.POST:
            t_id=request.POST['tid']
            p_id=request.POST['pid']

            TournamentPlayers.objects.filter(player_id=p_id,tournament_id=t_id).delete()
        

            
        else:
            player=request.POST['p']
            file=request.FILES['p_file']
            print('current count',current_count)
            print('allowed',tournament.players_allowed)
            exist=TournamentPlayers.objects.filter(tournament_id=id,player_id=player).exists()
            if not exist:
                print('current count',current_count+1)
                print('allowed',tournament.players_allowed)
                if current_count+1<=tournament.players_allowed:
                    tournament_id=TournamentDetails.objects.get(tournament_id=id)
                    player_id=PlayerDetails.objects.get(player_id=player)
                    team_id=TeamDetails.objects.get(team_id=request.session['team_id'])

                    data=TournamentPlayers(player_id=player_id,tournament_id=tournament_id,team_id=team_id,cert=file)
                    data.save()   
                    msg="Player Added Succesfully"
                else:
                    msg="Maximum Players Exceeded"
        
            else:
                msg="Player Already Added"

    if request.method=='GET':
         
        exist=TournamentRegistration.objects.filter(tournament_id=id,team_id=request.session['team_id']).exists()
        if not exist:
             
            tour=TournamentDetails.objects.get(tournament_id=id)
            team=TeamDetails.objects.get(team_id=request.session['team_id'])
            reg=TournamentRegistration(tournament_id=tour,team_id=team)
            reg.save()
    
    team_registered=TournamentRegistration.objects.filter(team_id=request.session['team_id'],tournament_id=id).exists()

    context={
        'tournament':tournament,
        'cur_players':current_players,
        'added_players':added_players,
        'msg':msg,
        'team_resgistered':team_registered,
        'approved':approved
            }
    return render(request,'TeamAdmin/TournamentPlayers.html',context)



def RegisteredTournaments(request):
    
    tournaments=TournamentRegistration.objects.filter(team_id=request.session['team_id'])
    return render(request,'TeamAdmin/TournamentRegistered.html',{'tournaments':tournaments,})


def Logout(request):
    del request.session['team_id']
    del request.session['team_type']
    request.session.flush()
    return redirect("club_management:home")