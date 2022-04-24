from datetime import date, datetime
from faulthandler import disable
from re import T
from django.db.models import Q
from time import strftime
from ClubManagementApp.Forms.TeamForm import AddPlayerForm
from django.shortcuts import render,redirect
from django.http import HttpResponse
from ..models import PlayerDetails,SportsDetail, TeamDetails, TournamentDetails, TournamentPlayers, TournamentRegistration,Fixture
from ..Forms import TeamForm
from passlib.hash import pbkdf2_sha256
from django.utils.crypto import get_random_string


def TeamHome(request):
    players=PlayerDetails.objects.filter(team_id=request.session['team_id']).count()
    return render(request,'TeamAdmin/TeamHome.html',{'players':players,})


def AddPlayer(request):
   
    
    form=AddPlayerForm()
    data=SportsDetail.objects.get(sport_id=request.session['team_type'])
    sport_type=data.sport_name
    if sport_type=='cricket':
        positions=['Batsman','Bowler','Wicket Keeper','All Rounder']
    elif sport_type=="football":
        positions=['striker','mid-fielder','defender','right wing back','goal keeper']
    

    if request.method=='POST':
        
        
        team_id=TeamDetails.objects.get(team_id=request.session['team_id'])
        player_name=request.POST['p_name'].lower()
        player_address=request.POST['p_addr'].lower()
        player_dob=request.POST['p_dob']
        player_email=request.POST['p_email']
        player_height=request.POST['p_height']
        player_weight=request.POST['p_weight']
        player_img=request.FILES['p_img']
        player_ph=request.POST['p_phno']
        player_position=request.POST['position']
        dt_con=datetime.strptime(player_dob,'%Y-%m-%d').date()
        dob=str(dt_con.day)+'/'+str(dt_con.month)+'/'+str(dt_con.year)
        passwd=get_random_string(length=8)
        player_passwd=pbkdf2_sha256.hash(passwd,rounds=1000,salt_size=32)
        email_exists=PlayerDetails.objects.filter(player_email=player_email).exists()
        
        if email_exists:
            err_msg="Email Already Exists"
            return render(request,'TeamAdmin/AddPlayer.html',{'form':form,'positions':positions,'err_msg':err_msg})
        
        phno_exists=PlayerDetails.objects.filter(player_ph=player_ph).exists()
        if phno_exists:
            err_msg="Phone No. Already Exists"
            return render(request,'TeamAdmin/AddPlayer.html',{'form':form,'positions':positions,'err_msg':err_msg})

        qry=PlayerDetails(team_id=team_id,player_name=player_name,player_address=player_address,player_dob=dob,player_email=player_email,player_ph=player_ph,player_position=player_position,player_height=player_height,player_weight=player_weight,player_img=player_img,player_passwd=player_passwd)
        qry.save()
        succ_msg="Player Added Succesfully"
        print('passwd is',passwd)
        #email_player(player_email,player_ph,passwd)
            
        return render(request,'TeamAdmin/AddPlayer.html',{'form':form,'positions':positions,'succ_msg':succ_msg})
         
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
    
    
    
    
    return render(request,'TeamAdmin/ViewTournaments.html',{'tournaments':tournament_data,})


def TournamentDetail(request,t_id):

    if request.method=='POST':
        print('here')
        if 'register' in request.POST:
            print('success')
            tournament=TournamentDetails.objects.get(tournament_id=t_id)
            team=TeamDetails.objects.get(team_id=request.session['team_id'])
            registration=TournamentRegistration(tournament_id=tournament,team_id=team)
            registration.save()

         

    tournament_data=TournamentDetails.objects.get(tournament_id=t_id)
    is_registered=TournamentRegistration.objects.filter(tournament_id=t_id,team_id=request.session['team_id']).exists()
    if is_registered == True:
        status='Registered'
        color="green"
    else:
        status='Not Registered'
        color='red'
    
    
    return render(request,'TeamAdmin/TournamentDetails.html',{'tournament':tournament_data,'status':status,'color':color})


def AddTournamentPlayers(request,id):

  

    tournament=TournamentDetails.objects.get(tournament_id=id)
    regstn=TournamentRegistration.objects.get(tournament_id=id,team_id=request.session['team_id'])
    current_players=PlayerDetails.objects.filter(team_id=request.session['team_id'])
    added_players=TournamentPlayers.objects.filter(team_id=request.session['team_id'])
    succ_msg=""
    err_msg=""
    current_count=TournamentPlayers.objects.filter(tournament_id=tournament.tournament_id,team_id=request.session['team_id']).count()
    approved=False
    for p in added_players:
        
        if p.player_status=='not approved' or p.player_status=='rejected':
            
            approved=True
            break 

    
    if request.method=='POST':

         

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
                    succ_msg="Player Added Succesfully"
                    tournament=TournamentDetails.objects.get(tournament_id=id)
                    regstn=TournamentRegistration.objects.get(tournament_id=id,team_id=request.session['team_id'])
                    current_players=PlayerDetails.objects.filter(team_id=request.session['team_id'])
                    added_players=TournamentPlayers.objects.filter(team_id=request.session['team_id'])
                     
                    err_msg=""
                    current_count=TournamentPlayers.objects.filter(tournament_id=tournament.tournament_id,team_id=request.session['team_id']).count()
                    approved=False
                    for p in added_players:
                        
                        if p.player_status=='not approved' or p.player_status=='rejected':
                            
                            approved=True
                            break    

                else:
                    err_msg="Maximum Players Exceeded"
        
            else:
                err_msg="Player Already Added"

    # if request.method=='GET':
         
    #     exist=TournamentRegistration.objects.filter(tournament_id=id,team_id=request.session['team_id']).exists()
    #     if not exist:
             
    #         tour=TournamentDetails.objects.get(tournament_id=id)
    #         team=TeamDetails.objects.get(team_id=request.session['team_id'])
    #         reg=TournamentRegistration(tournament_id=tour,team_id=team)
    #         reg.save()
           
    #         print('redirecting')
    #         return redirect('TeamHome/T-Players',id)
    team_registered=TournamentRegistration.objects.filter(team_id=request.session['team_id'],tournament_id=id).exists()

    context={
        'tournament':tournament,
        'cur_players':current_players,
        'reg':regstn,
        'added_players':added_players,
        'succ_msg':succ_msg,
        'err_msg':err_msg,
        'team_resgistered':team_registered,
        'approved':approved
            }
    return render(request,'TeamAdmin/TournamentPlayers.html',context)



def RegisteredTournaments(request):
    
    tournaments=TournamentRegistration.objects.filter(team_id=request.session['team_id'])
    return render(request,'TeamAdmin/TournamentRegistered.html',{'tournaments':tournaments,})


def Fixtures(request,tid):
    return render(request,'TeamAdmin/Fixtures.html')

def LiveMatch(request,tid):
    return render(request,'TeamAdmin/LiveMatch.html')

def MatchStatus(request,tid):
    return render(request,'TeamAdmin/MatchStatus.html')

def PointsTable(request):
    tournaments=TournamentDetails.objects.filter(tournament_status='not completed')
    if request.method=='POST':
        data=TournamentRegistration.objects.filter(tournament_id=request.POST['tr']).order_by('-team_point')
        tr=TournamentDetails.objects.get(tournament_id=request.POST['tr'])
        return render(request,'TeamAdmin/PointTable.html',{'tournaments':tournaments,'data':data,'tr':tr})
    return render(request,'TeamAdmin/PointTable.html',{'tournaments':tournaments})

def PreviousMatches(request):
    matches=Fixture.objects.filter(Q(team1=request.session['team_id'])|Q(team2=request.session['team_id']))
    if request.method=='POST':
        id=request.POST['id']
        m=Fixture.objects.get(id=id)
        return render(request,'TeamAdmin/PreviousVideo.html',{'m':m,})

    return render(request,'TeamAdmin/PreviousMatches.html',{'matches':matches,})

def Logout(request):
    del request.session['team_id']
    del request.session['team_type']
    request.session.flush()
    return redirect("club_management:home")


def TournamentStatus(request):
     
    tournaments=TournamentDetails.objects.filter(tournament_status='not completed')
    if request.method=='POST':
        tr=request.POST['tr']
         
        matches=Fixture.objects.filter(tournament_id=tr)

         

        return render(request,'Admin/TournamentStatus.html' ,{'tournaments':tournaments,'matches':matches,})
    return render(request,'TeamAdmin/TournamentStatus.html' ,{'tournaments':tournaments,})

