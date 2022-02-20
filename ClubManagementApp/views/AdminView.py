from time import strftime
from ClubManagementApp.services import account_status
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.db.models import Q
from datetime import date, datetime
from ..models import AdminNotification,SportsDetail, TeamDetails, VenueDetails,TournamentDetails
from ClubManagementApp.Forms.AdminForm import *

def AdminHome(request):
    return render(request,'Admin/AdminHome.html')

def AddSport(request):
    form=AddSportForm()
    sports_data=SportsDetail.objects.all()
    if request.method=='POST':
        form=AddSportForm(request.POST)
        if form.is_valid():
            sport_name=form.cleaned_data['sport_name']
            sport_type=form.cleaned_data['sport_type']
            do_exist=SportsDetail.objects.filter(sport_name=sport_name.lower(),sport_type=sport_type).exists()
            if do_exist:
                error_msg="Sport Already Added"
                return render(request,'Admin/AddSports.html',{'form':form,'error_msg':error_msg,'sports':sports_data})
            else:
                qry=SportsDetail(sport_name=sport_name.lower(),sport_type=sport_type)
                qry.save()
                success_msg="Sport Added Succesfully"
                return render(request,'Admin/AddSports.html',{'form':form,'success_msg':success_msg,'sports':sports_data})
    return render(request,'Admin/AddSports.html',{'form':form,'sports':sports_data})



def PendingTeamRequest(request):
    teams=TeamDetails.objects.filter(team_status='not approved')
    return render(request,'Admin/PendingTeamRequest.html',{'teams':teams})

def PendingVenueRequest(request):
    venue=VenueDetails.objects.filter(venue_status='not approved')
    print(venue)
    return render(request,'Admin/PendingVenueRequest.html',{'venues':venue})



def  ApproveTeam(request,id):
    team_data=TeamDetails.objects.get(team_id=id)
    team_data.team_status="approved"
    team_data.save()
    account_status(team_data.team_email,"Approved")
    return redirect("club_management:team_request") 

def  RejectTeam(request,id):
    team_data=TeamDetails.objects.get(team_id=id)
    team_data.delete()
    account_status(team_data.team_email,"Reject")
    return redirect("club_management:team_request") 

def  ApproveVenue(request,id):
    venue_data=VenueDetails.objects.get(venue_id=id)
    venue_data.venue_status="approved"
    venue_data.save()
    account_status(venue_data.venue_email,"Approved")
    return redirect("club_management:venue_request") 

def  RejectVenue(request,id):
    venue_data=VenueDetails.objects.get(venue_id=id)
    venue_data.delete()
    account_status(venue_data.venue_email,"Reject")
    return redirect("club_management:venue_request") 


def ViewTeams(request):
    teams=TeamDetails.objects.filter(team_status="approved")
    return render(request,'Admin/ViewTeams.html',{'teams':teams})

def ViewVenue(request):
    venues=VenueDetails.objects.filter(venue_status="approved")
    return render(request,'Admin/ViewVenue.html',{'venues':venues})



def AddNotification(request):
    form=AdminNotificationform()
    if request.method=='POST':
        form=AdminNotificationform(request.POST)
        if form.is_valid():
            print('valid')
            notfn_title=form.cleaned_data['notfn_title']
            notfn_text=form.cleaned_data['notfn_content']
            notfn_date=date.today()
            qry=AdminNotification(notfn_title=notfn_title,notfn_date=notfn_date,notfn_content=notfn_text)
            qry.save()
            msg="Notification Submitted Succesfully"
            return render(request,'Admin/AddNotifications.html',{'form':form,'msg':msg})
        else:
            print(form.errors)
    return render(request,'Admin/AddNotifications.html',{'form':form})

def ViewBlock(request,venue_id):
    block_data=BlockDetails.objects.get(venue_id=venue_id)
    print(block_data.venue_id.venue_pic.url)
    return render(request,'Admin/BlockDetails.html',{'block_data':block_data})

def ViewPlayers(request,team_id):
    players_list=PlayerDetails.objects.filter(team_id=team_id)
    return render(request,'Admin/ViewPlayers.html',{'players':players_list})

def AddTournament(request):
    
    sport_type=SportsDetail.objects.all()
    # dt="23/02/2022"
    # con_dt=datetime.strptime(dt,"%d/%m/%Y")
    # print(type(con_dt))
    # print(dt==strftime("%d/%m/%Y"))
    
    if request.method=='POST':
        
       
        
            
        dt=strftime("%d/%m/%Y")
        cur_date=datetime.strptime(dt,'%d/%m/%Y').date()


        tournament_title=request.POST['t_title']
        venue_id=VenueDetails.objects.get(venue_id=request.POST['venue_list'])
        sport_id=SportsDetail.objects.get(sport_id=request.POST['sport'])
        players_allowed=request.POST['p_no']
        # start_date=datetime.strptime(request.POST['s_date'],'%Y/%M/%d')
        # end_date=datetime.strptime(request.POST['e_date'],'%Y/%m/%d')
        # reg_date=datetime.strptime(request.POST['l_date'],'%Y/%m/%d')
        start_date=request.POST['s_date']
        end_date=request.POST['e_date']
        reg_date=request.POST['l_date']
        reg_fee=request.POST['reg_fee']
        win_prize=request.POST['p_money']

        st_con=datetime.strptime(start_date,'%Y-%m-%d').date()
        en_con=datetime.strptime(end_date,'%Y-%m-%d').date()
        reg_con=datetime.strptime(reg_date,'%Y-%m-%d').date()

        print('start date',start_date)
        print('end date',end_date)
        print('reg date',reg_date)

        print('start date',st_con)
        print('end date',en_con)
        print('reg date',reg_con)

        print('dddddddddd',type(start_date))
        if st_con<cur_date:
            msg="Invalid Date Selection"
            print('first')
            return render(request,'Admin/TournamentAdd.html',{'sport_type':sport_type,'msg':msg})  

        elif st_con>en_con:
            print('second')
            msg="Invalid Date Selection"
            return render(request,'Admin/TournamentAdd.html',{'sport_type':sport_type,'msg':msg})  
        
        elif reg_con>st_con or reg_con>en_con:
            print('third') 
            msg="Invalid Date Selection"
            return render(request,'Admin/TournamentAdd.html',{'sport_type':sport_type,'msg':msg})   
        else:
            qry=TournamentDetails(tournament_title=tournament_title,venue_id=venue_id,sport_type=sport_id,players_allowed=players_allowed,start_date=start_date,end_date=end_date,reg_date=reg_date,reg_fee=reg_fee,win_prize=win_prize,tournament_status="not completed")
            qry.save()
            msg="Tournament Added Succesfully"  
            return render(request,'Admin/TournamentAdd.html',{'sport_type':sport_type,'msg':msg})  
    return render(request,'Admin/TournamentAdd.html',{'sport_type':sport_type})

def getVenue(request):
    sport_id=request.GET.get('sport_id')
    sport=SportsDetail.objects.get(sport_id=sport_id)
    sport_name=sport.sport_name
    print(sport_name)
    venue_list=VenueDetails.objects.filter(Q(venue_type=sport_name)|Q(venue_type="both"))
    
    return render(request, 'Admin/venue_list.html',{'venue_list':venue_list})


def TournamentRequest(request):
    t_data=TournamentDetails.objects.filter(tournament_status="not completed")
    team_reg=1
    return render(request, 'Admin/TournamentRequest.html',{'t_data':t_data})