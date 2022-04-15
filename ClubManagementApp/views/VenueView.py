from ClubManagementApp.Forms.VenueForm import BlockForm
from django.shortcuts import render,redirect
from django.http import HttpResponse
from ..models import BlockDetails, VenueDetails


def VenueHome(request):
    return render(request,'Venue/VenueHome.html')

def AddBlock(request):
    form=BlockForm()
    if request.method=='POST':
        form=BlockForm(request.POST)
        if form.is_valid():
            block_name=form.cleaned_data['block_title'].lower()
            amount=form.cleaned_data['amount']
            seats=form.cleaned_data['total_seats']

            data_exist=BlockDetails.objects.filter(venue_id=request.session['venue_id'],block_title=block_name).exists()
            if not data_exist:
                venue=VenueDetails.objects.get(venue_id=request.session['venue_id'])
                qry=BlockDetails(venue_id=venue,block_title=block_name,amount=amount,total_seats=seats)
                qry.save()
                msg="Block Added Succesfully"
                return render(request,'Venue/AddBlock.html',{'form':form,'msg':msg})
            else:
                msg="Block Already Added"
                return render(request,'Venue/AddBlock.html',{'form':form,'msg':msg})
    return render(request,'Venue/AddBlock.html',{'form':form})

def ViewBlock(request):
    data=BlockDetails.objects.filter(venue_id=request.session['venue_id'])
     
    return render(request,'Venue/ViewBlock.html',{'data':data})

def ViewBooking(request):
    block=BlockDetails.objects.filter(venue_id=request.session['venue_id'])
    return render(request,'Venue/ViewBooking.html',{'block':block})

def ChangePassword(request):
    
    return render(request,'Venue/ChangePassword.html')

def VenueRequest(request):
    
    return render(request,'Venue/VenueRequest.html')

def RejectReason(request):
    
    return render(request,'Venue/RejectReason.html')
