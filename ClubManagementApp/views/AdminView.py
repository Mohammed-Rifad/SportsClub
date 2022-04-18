from re import T
from time import strftime

from django.http import JsonResponse
from ClubManagementApp.services import FixtureGenerate, account_status
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.db.models import Q
from datetime import date, datetime, timedelta
from ..models import AdminNotification,SportsDetail, TeamDetails, VenueDetails,TournamentDetails,Fixture
from ClubManagementApp.Forms.AdminForm import *

def AdminHome(request):
    count=VenueDetails.objects.filter(venue_status="approved").count()
    notfn=AdminNotification.objects.all()[:5]
    pending_teams=TeamDetails.objects.filter(team_status='not approved').count()
    approved_teams=TeamDetails.objects.filter(team_status='approved').count()
    ongoing_tournaments=TournamentDetails.objects.filter(tournament_status='not completed')
    
    return render(request,'Admin/AdminHome.html',{'count':count,'ongoing_tournaments':ongoing_tournaments,'notfn':notfn,'p_count':pending_teams,
    'app_count':approved_teams
    })

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
    # account_status(team_data.team_email,"Approved")
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
 
        notfn_title=request.POST['notfn_title']
        notfn_text=request.POST['notfn_content']
        notfn_date=date.today()
        d=notfn_date.strftime('%Y-%m-%d')
        st_con=datetime.strptime(d,'%Y-%m-%d').date()
        st_dt=str(st_con.day)+'/'+str(st_con.month)+'/'+str(st_con.year)
        qry=AdminNotification(notfn_title=notfn_title,notfn_date=st_dt,notfn_content=notfn_text)
        qry.save()
        msg="Notification Submitted Succesfully"
        return render(request,'Admin/AddNotifications.html',{'form':form,'msg':msg})
        
    return render(request,'Admin/AddNotifications.html',{'form':form})

def ViewBlock(request,venue_id):
    block_data=BlockDetails.objects.get(venue_id=venue_id)
    print(block_data.venue_id.venue_pic.url)
    return render(request,'Admin/BlockDetails.html',{'block_data':block_data})

def ViewPlayers(request,team_id):
    players_list=PlayerDetails.objects.filter(team_id=team_id)
    team=TeamDetails.objects.get(team_id=team_id)
    return render(request,'Admin/ViewPlayers.html',{'players':players_list,'team':team.team_name})

def AddTournament(request):
     
    sport_type=SportsDetail.objects.all()
     
     
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

         
        if st_con<cur_date:
            err_msg="Invalid Date Selection"
            print('first')
            return render(request,'Admin/TournamentAdd.html',{'sport_type':sport_type,'err_msg':err_msg,'is_display':True})  

        elif st_con>en_con:
            print('second')
            err_msg="Invalid Date Selection"
            return render(request,'Admin/TournamentAdd.html',{'sport_type':sport_type,'err_msg':err_msg, 'is_display':True})  
        
        elif reg_con<st_con or reg_con>en_con:
            print('third')
            err_msg="Invalid Date Selection"
            return render(request,'Admin/TournamentAdd.html',{'sport_type':sport_type, 'err_msg':err_msg,'is_display':True})   
        else:
            st_dt=str(st_con.day)+'/'+str(st_con.month)+'/'+str(st_con.year)
            en_dt=str(en_con.day)+'/'+str(en_con.month)+'/'+str(en_con.year)
            reg_dt=str(reg_con.day)+'/'+str(reg_con.month)+'/'+str(reg_con.year)

            qry=TournamentDetails(tournament_title=tournament_title,venue_id=venue_id,sport_type=sport_id,players_allowed=players_allowed,start_date=st_dt,end_date=en_dt,reg_date=reg_dt,reg_fee=reg_fee,win_prize=win_prize,tournament_status="not completed")
            qry.save()
            msg="Tournament Added Succesfully"  
             
            print('success')
            return render(request,'Admin/TournamentAdd.html',{'sport_type':sport_type,'msg':msg,'is_success':True})  
    return render(request,'Admin/TournamentAdd.html',{'sport_type':sport_type, })

def getVenue(request):
    sport_id=request.GET.get('sport_id')
    sport=SportsDetail.objects.get(sport_id=sport_id)
    sport_name=sport.sport_name
    print(sport_name)
    venue_list=VenueDetails.objects.filter(Q(venue_type=sport_name)|Q(venue_type="both"))
    
    return render(request, 'Admin/venue_list.html',{'venue_list':venue_list})


def TournamentRequest(request):
    
    t_data=TournamentDetails.objects.filter(tournament_status="not completed")
    return render(request, 'Admin/TournamentRequest.html',{'t_data':t_data})

def TournamentTeams(request):
    teams=TournamentRegistration.objects.filter(tournament_id=request.GET['id'])
    tr_name=TournamentDetails.objects.get(tournament_id=request.GET['id'])
    return render(request, 'Admin/RegTeam.html',{'teams':teams,'name':tr_name.tournament_title})

def ViewTournamentPlayers(request):
    if request.method=='POST':
         TournamentRegistration.objects.filter(tournament_id=request.session['tr'],team_id=request.session['t']).update(
             team_status='approved'
         )
         return redirect('club_management:admin_home')
    hide_btn=True
    if 't_id' in request.GET:
        team=request.GET['t_id']
        tournament=request.GET['tr_id']
        request.session['t']=team
        request.session['tr']=tournament
    players_list=TournamentPlayers.objects.filter(team_id=request.session['t'],tournament_id=request.session['tr'])
    for p in players_list:
        if p.player_status=='not approved' or p.player_status=='rejected':
            hide_btn=False
            print('here')
            break
    
    return render(request, 'Admin/TrTeamPlayers.html',{'players_list':players_list,'hide_btn':hide_btn})

def UpdatePlayerStatus(request):

    player=request.POST['pl']
    if 'approve' in request.POST:
        record=TournamentPlayers.objects.get(player_id=player,tournament_id=request.session['tr'])
        record.player_status='approved'
        record.save()
        return redirect('club_management:a_viewtrTeam')

    if 'reject' in request.POST:
        record=TournamentPlayers.objects.get(player_id=player,tournament_id=request.session['tr'])
        record.player_status='rejected'
        record.save()
        return redirect('club_management:a_viewtrTeam')


def GenerateFixture(request):
    tr_data=TournamentDetails.objects.filter(tournament_status='not completed')
    dt_dict={}
    dt_arr=[]
    fixture_data=""
    if request.method=='POST':

        if 'upd' in request.POST:
            id=request.POST['tr']
            return redirect('/SCMS/AdminHome/Fixture/'+id)
        else:

            tr=TournamentRegistration.objects.filter(tournament_id=request.POST['tr'])
            dt=TournamentDetails.objects.get(tournament_id=request.POST['tr'])
            
            dt_start=datetime.strptime(dt.start_date,'%d/%m/%Y')
            dt_end=datetime.strptime(dt.end_date,'%d/%m/%Y')

            diff=dt_end-dt_start
            
            for x in range(0,diff.days+1):
                print(dt_start+timedelta(days=x),'  ',dt_end)
                # d=str(dt_start.day)+'/'+str(dt_start.month)+'/'+str(dt_start.year)
                st=dt_start+timedelta(days=x)
                dt_dict['date']=str(st.day)+'/'+str(st.month)+'/'+str(st.year)
                dt_arr.append(dt_dict)
                dt_dict={}
            print(dt_arr)
            fxt=FixtureGenerate(tr,tr.count())
            
            fixture_generated=Fixture.objects.filter(tournament_id=request.POST['tr']).exists()

            if not fixture_generated:
                for i in fxt:
                    
                    fixture=Fixture(tournament_id=dt,team1=i['t1'],team2=i['t2'],match=i['match'])
                    fixture.save()

                # print(i['t1'])

            fixture_data=Fixture.objects.filter(tournament_id=request.POST['tr'])
                
            

            
    return render(request,'Admin/GenerateFixture.html',{'tr_data':tr_data,'fixture':fixture_data,'date':dt_arr})

def UpdateFixture(request,id):

    dt_arr=[]
    dt_dict={}
    fixtures=Fixture.objects.filter(tournament_id=id)    
    dt=TournamentDetails.objects.get(tournament_id=id)
    dt_start=datetime.strptime(dt.start_date,'%d/%m/%Y')
    dt_end=datetime.strptime(dt.end_date,'%d/%m/%Y')

    diff=dt_end-dt_start
    
    for x in range(0,diff.days+1):
        print(dt_start+timedelta(days=x),'  ',dt_end)
        # d=str(dt_start.day)+'/'+str(dt_start.month)+'/'+str(dt_start.year)
        st=dt_start+timedelta(days=x)
        dt_dict['date']=str(st.day)+'/'+str(st.month)+'/'+str(st.year)
        dt_arr.append(dt_dict)
        dt_dict={}

    if request.method=='POST':
        date=request.POST['dt']
        match=request.POST['match']
        t1=request.POST['t1']
        t2=request.POST['t2']
        f=request.POST['am/pm']
        if int(t1)<1:
            t1='0'+t1
        if int(t2)<10:
            t2='0'+t2
        time=t1+':'+t2 +' '+f
        print(time)
        fxt=Fixture.objects.get(id=match)
        fxt.date=date
        fxt.time=time
        fxt.save()
    return render(request,'Admin/UpdateFixture.html',{'fixtures':fixtures,'tr':dt,'date':dt_arr})
    
def UploadLive(request):
    tournaments=TournamentDetails.objects.filter(tournament_status='not completed')

    if request.method=='POST':
       
        fx=Fixture.objects.get(id=request.POST['fx'])
        fx.match_video=request.FILES['file']
        fx.save()
        succ_msg='Video Uploaded Succesfully'
        return render(request,'Admin/UploadLive.html',{'tournaments':tournaments,'succ_msg':succ_msg,})
    return render(request,'Admin/UploadLive.html',{'tournaments':tournaments,})

def LoadTournaments(request):
    id=request.POST['id']
    tr=Fixture.objects.filter(tournament_id=id)
     
    
    return render(request,'Admin/Matches.html',{'tr':tr,})

def MatchStatus(request):
    tournaments=TournamentDetails.objects.filter(tournament_status='not completed')
    
    if request.method=='POST':
        fx=request.POST['fx']
        score1=request.POST['t_score1']
        score2=request.POST['t_score2']
        res=request.POST['result'].lower()
        wonby=request.POST['wonby']
        
        tr_reg=TournamentRegistration.objects.get(tournament_id=request.POST['tr'],team_id=wonby)
        tr_reg.team_point+=1
        tr_reg.save()
        fixture=Fixture.objects.get(id=fx)

        fixture.team1_score=score1
        fixture.team2_score=score2
        fixture.result=res

        fixture.save()
        succ_msg="Updated Succesfully"
        return render(request,'Admin/MatchStatus.html' ,{'tournaments':tournaments,'succ_msg':succ_msg,})

    return render(request,'Admin/MatchStatus.html' ,{'tournaments':tournaments,})


def TournamentStatus(request):
     
    tournaments=TournamentDetails.objects.filter(tournament_status='not completed')
    if request.method=='POST':
        tr=request.POST['tr']
         
        matches=Fixture.objects.filter(tournament_id=tr)

         

        return render(request,'Admin/TournamentStatus.html' ,{'tournaments':tournaments,'matches':matches,})
    return render(request,'Admin/TournamentStatus.html' ,{'tournaments':tournaments,})

def UpdateTrStatus(request):

    tr=request.POST['tr_id']
    tournament=TournamentDetails.objects.get(tournament_id=tr)
    tournament.tournament_status='completed'
    tournament.save()

    return redirect('club_management:admin_home')

def LoadTeam(request):
    fx=Fixture.objects.get(id=request.POST['id'])
     
    return render(request,'Admin/LoadTeam.html',{'t':fx,})