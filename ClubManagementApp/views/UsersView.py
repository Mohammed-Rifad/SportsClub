from datetime import datetime
from threading import current_thread
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from ClubManagementApp.models import Booking, BlockDetails,  Fixture, MemberDetails, TournamentDetails, VenueDetails
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
    booking_data = Booking.objects.filter(m_id=request.session['member_id'])
    return render(request, 'Member/BookingHistory.html', {'booking_data': booking_data})


def WatchVideo(request, id):
    fx = None
    fx = Fixture.objects.get(id=id)
    
    return render(request, 'Member/WatchVideo.html', {'fx': fx})

def Vote(request):
    print(request.POST['fx_id'])
    return JsonResponse({'response':'hgfh3e'})