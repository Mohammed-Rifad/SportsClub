from django.shortcuts import render,redirect
from django.http import HttpResponse



def PlayerHome(request):
    print(request.session['player_id'])
    return render(request,'Players/PlayerHome.html')