from datetime import datetime
import re
from threading import current_thread
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from ClubManagementApp.models import Booking, BlockDetails,  Fixture, MemberDetails, TeamDetails, TournamentDetails, VenueDetails, Vote
from ClubManagementApp.services import BookingNumber


def MemberHome(request):

    return render(request, 'Member/MemberHome.html')


def LoadRecentTournament(request):
    data = TournamentDetails.objects.filter(tournament_status='not completed')
    return render(request, 'Member/RecentTournament.html', {'data': data, })


def LoadFixture(request, id):
    fixture_set = Fixture.objects.filter(tournament_id=id)
    tournament = TournamentDetails.objects.get(tournament_id=id)
    venue = tournament.venue_id
    return render(request, 'Member/Fixture.html', {'fixture': fixture_set, 'tournament': tournament, 'venue': venue})


def BookTicket(request, id):
    tr_id = request.GET['tr']

    member = MemberDetails.objects.get(m_id=request.session['member_id'])
    tournament = TournamentDetails.objects.get(tournament_id=tr_id)
    venue_details = VenueDetails.objects.get(
        venue_id=tournament.venue_id.venue_id)
    block_details = BlockDetails.objects.filter(
        venue_id=venue_details.venue_id)

    return render(request, 'Member/BookTicket.html', {'venue': venue_details, 'block_details': block_details, 'member': member, 'tr': tr_id, 'fx': id})


def Checkout(request, id):
    block = BlockDetails.objects.get(id=request.GET['b'])
    tr = request.GET['tr']
    fx = id
    venue = request.GET['v']
    amount = block.amount
    member = MemberDetails.objects.get(m_id=request.session['member_id'])
    print(block.id)
    return render(request, 'Member/Checkout.html', {'amount': amount, 'member': member, 'tr': tr, 'fx': fx, 'b': block, 'venue': venue})


def CheckoutProceed(request):

    tournament = TournamentDetails.objects.get(tournament_id=request.GET['tr'])
    block = BlockDetails.objects.get(id=request.GET['b'])
    fixture = Fixture.objects.get(id=request.GET['f'])
    total = request.GET['t']
    tickets = request.GET['tic']
    venue = VenueDetails.objects.get(venue_id=request.GET['v'])
    m_id = MemberDetails.objects.get(m_id=request.session['member_id'])
    book_no = BookingNumber(tournament, 'offline')
    payment = Booking(tournament_id=tournament, fix_id=fixture, m_id=m_id, type='offline', venue=venue, block=block, total=total, tickets=tickets,
                      book_number=book_no)
    payment.save()
    return redirect('club_management:member_home')


def CheckoutOnline(request):
    venue = VenueDetails.objects.get(venue_id=request.GET['venue'])
    tr = TournamentDetails.objects.get(tournament_id=request.GET['tr'])
    fx = Fixture.objects.get(id=request.GET['fx'])
    type = 'online'
    member = MemberDetails.objects.get(m_id=request.session['member_id'])
    total = 300
    book_no = BookingNumber(tr, 'online')
    payment = Booking(tournament_id=tr, venue=venue, fix_id=fx,
                      m_id=member, total=total, type=type, book_number=book_no)
    payment.save()
    return redirect('club_management:member_home')


def BookingHistory(request):
    booking_data = Booking.objects.filter(m_id=request.session['member_id'],type='online')
    return render(request, 'Member/BookingHistory.html', {'booking_data': booking_data})


def WatchVideo(request, id):
    fx = None
    team_voted=None
    fx = Fixture.objects.get(id=id)
    try:
        vote_data=Vote.objects.get(fix_id=id,m_id=request.session['member_id'])
        team_voted=vote_data.team.team_id
         
    except:
        pass
    return render(request, 'Member/WatchVideo.html', {'fx': fx,'team_voted':team_voted})

def UserVote(request):
    print(request.POST['fx_id'])
    fixture=Fixture.objects.get(id=request.POST['fx_id'])
    tr=fixture.tournament_id.tournament_id
    member=MemberDetails.objects.get(m_id=request.session['member_id'])
   
    team=TeamDetails.objects.get(team_id=request.POST['team'])
    already_voted=Vote.objects.filter(m_id=request.session['member_id'],fix_id=request.POST['fx_id']).exists()
    if already_voted:
        Vote.objects.filter(m_id=request.session['member_id'],fix_id=request.POST['fx_id']).update(team=team)
    else:

        vote=Vote(fix_id=fixture,m_id=member,vote=1,team=team)
        vote.save()
    return JsonResponse({'voted_team':team.team_id})

def ChangePassword(request):
    if request.method=='POST':
        old_passwd=request.POST['old_passwd']
        new_passwd=request.POST['new_passwd']
        conf_passwd=request.POST['conf_passwd']
        member_data=MemberDetails.objects.get(m_id=request.session['member_id'])
        if member_data.verifyPasswd(old_passwd):
            if new_passwd==conf_passwd:
                if len(new_passwd)<8:
                    err_msg='Password Should be minimum 8 characters'
                    return render(request,'Member/ChangePassword.html',{'err_msg':err_msg})
                else:
                    member_data.m_passwd=new_passwd
                    member_data.save()
                    succ_msg='Password Changed Succesfully'
                    return render(request,'Member/ChangePassword.html',{'succ_msg':succ_msg})
            else:
                print('kdjhe')
                err_msg='Password Doesn\'t Match'
                return render(request,'Member/ChangePassword.html',{'err_msg':err_msg})
        else:
                err_msg='Wrong Password'
                return render(request,'Member/ChangePassword.html',{'err_msg':err_msg})
    return render(request,'Member/ChangePassword.html')