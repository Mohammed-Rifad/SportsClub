from ClubManagementApp.Forms.VenueForm import VenueRegForm
from passlib.hash import pbkdf2_sha256
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from ..services import GetTeamID, GetvenueID, email_team
from ..models import AdminDetails, TeamDetails, SportsDetail, AdminNotification
from ..Forms.AdminForm import *
from ..Forms.TeamForm import *


def AdminData(request):
    passwd = pbkdf2_sha256.hash("admin", rounds=1000, salt_size=32)
    qry = AdminDetails(login_id="Admin", login_passwd=passwd)
    qry.save()
    return redirect("club_management:login")


def ProjectHome(request):
    latest_notification = AdminNotification.objects.latest('notfn_id')
    latest_notification = str(latest_notification.notfn_content)
    return render(request, 'Common/ProjectHome.html', {'notification': latest_notification})


def Login(request):
    form = LoginForm()

    if request.method == 'POST':
        login_id = request.POST['login_id']
        form = LoginForm(request.POST)
        if login_id == 'Admin':

            if form.is_valid():
                login_id = form.cleaned_data['login_id']
                login_passwd = form.cleaned_data['login_passwd']
                auth_check = AdminDetails.objects.filter(
                    login_id=login_id).exists()

                if auth_check:
                    auth_data = AdminDetails.objects.get(login_id=login_id)
                    auth_passwd = auth_data.verifyPasswd(login_passwd)
                    if auth_passwd:

                        return redirect("club_management:admin_home")
                    else:
                        msg = "Incorrect Password"
                    return render(request, 'Common/CommonLogin.html', {'form': form, 'msg': msg, })
                else:
                    msg = "Incorrect UserName or Password"

                    return render(request, 'Common/CommonLogin.html', {'form': form, 'msg': msg, })

        elif ((login_id.isdigit() == True) and (len(login_id) == 4)):

            if form.is_valid():
                login_id = form.cleaned_data['login_id']
                login_passwd = form.cleaned_data['login_passwd']
                auth_check = TeamDetails.objects.filter(
                    team_user_id=login_id).exists()
                if auth_check:
                    auth_data = TeamDetails.objects.get(team_user_id=login_id)
                    auth_passwd = auth_data.verifyPasswd(login_passwd)
                    if auth_passwd:
                        if auth_data.team_status == 'approved':
                            request.session['team_id'] = auth_data.team_id
                            request.session['team_name'] = auth_data.team_name
                            request.session['team_type'] = auth_data.team_type.sport_id
                            return redirect("club_management:team_home")
                        else:
                            msg = "Account Not Approved Yet"
                            return render(request, 'Common/CommonLogin.html', {'form': form, 'msg': msg, })
                    else:
                        msg = "Incorrect Password"
                    return render(request, 'Common/CommonLogin.html', {'form': form, 'msg': msg, })
                else:
                    msg = "Incorrect UserName or Password"
                    print('h')
                    return render(request, 'Common/CommonLogin.html', {'form': form, 'msg': msg, })
        elif ((login_id.isdigit() == True) and (len(login_id) == 10)):

            if form.is_valid():
                login_id = form.cleaned_data['login_id']
                login_passwd = form.cleaned_data['login_passwd']
                auth_check = PlayerDetails.objects.filter(
                    player_ph=login_id).exists()
                if auth_check:
                    auth_data = PlayerDetails.objects.get(player_ph=login_id)
                    auth_passwd = auth_data.verifyPasswd(login_passwd)
                    if auth_passwd:

                        request.session['player_id'] = auth_data.player_id
                        request.session['team_position'] = auth_data.player_position
                        return redirect("club_management:player_home")

                    else:
                        msg = "Incorrect Password"
                    return render(request, 'Common/CommonLogin.html', {'form': form, 'msg': msg, })
                else:
                    msg = "Incorrect UserName or Password"
                    print('h')
                    return render(request, 'Common/CommonLogin.html', {'form': form, 'msg': msg, })

        elif ((login_id.isdigit() == True) and (len(login_id) == 5)):

            if form.is_valid():
                login_id = form.cleaned_data['login_id']
                login_passwd = form.cleaned_data['login_passwd']
                auth_check = VenueDetails.objects.filter(
                    venue_user_id=login_id).exists()
                if auth_check:
                    auth_data = VenueDetails.objects.get(
                        venue_user_id=login_id)
                    auth_passwd = auth_data.verifyPasswd(login_passwd)
                    if auth_passwd:
                        if auth_data.venue_status == 'approved':
                            request.session['venue_id'] = auth_data.venue_id
                            request.session['venue_type'] = auth_data.venue_type
                            return redirect("club_management:venue_home")
                        else:
                            msg = "Account Not Approved Yet"
                            return render(request, 'Common/CommonLogin.html', {'form': form, 'msg': msg, })
                    else:
                        msg = "Incorrect Password"
                    return render(request, 'Common/CommonLogin.html', {'form': form, 'msg': msg, })
                else:
                    msg = "Incorrect UserName or Password"

                    return render(request, 'Common/CommonLogin.html', {'form': form, 'msg': msg, })
        elif '@' in login_id:

            if form.is_valid():
                print('000000000000000000000000000')
                login_id = form.cleaned_data['login_id']
                login_passwd = form.cleaned_data['login_passwd']
                auth_check = MemberDetails.objects.filter(
                    m_email=login_id).exists()
                print(auth_check)
                if auth_check:
                    auth_data = MemberDetails.objects.get(m_email=login_id)
                    auth_passwd = auth_data.verifyPasswd(login_passwd)
                    if auth_passwd:

                        request.session['member_id'] = auth_data.m_id

                        return redirect("club_management:member_home")

                    else:
                        msg = "Incorrect Password"
                    return render(request, 'Common/CommonLogin.html', {'form': form, 'msg': msg, })
                else:
                    msg = "Incorrect UserName or Password"

                    return render(request, 'Common/CommonLogin.html', {'form': form, 'msg': msg, })
    return render(request, 'Common/CommonLogin.html', {'form': form, })


def TeamReg(request):
    form = TeamRegForm()
    sport_types = SportsDetail.objects.all()
    if request.method == 'POST':

        team_name = request.POST['t_name'].lower()
        team_place = request.POST['t_place'].lower()
        team_phno = request.POST['t_phno']
        team_logo = request.FILES['t_logo']
        team_email = request.POST['t_email']
        id = request.POST['team_type']
        team_type = SportsDetail.objects.get(sport_id=id)
        team_status = "not approved"
        team_user_id = GetTeamID()
        passwd = get_random_string(length=8)
        team_passwd = pbkdf2_sha256.hash(passwd, rounds=1000, salt_size=32) # password encrypted using sha256
        do_exist = TeamDetails.objects.filter(
            team_name=team_name, team_place=team_place, team_type=id).exists()

        if do_exist:
            err_msg = "Team Name Already Taken"
            return render(request, 'Common/TeamRegistration.html', {'form': form, 'types': sport_types, 'err_msg': err_msg})
        else:
            email_exist = TeamDetails.objects.filter(
                team_email=team_email).exists()
            if not email_exist:
                qry = TeamDetails(team_name=team_name, team_place=team_place, team_email=team_email, team_type=team_type,
                                  team_phno=team_phno, team_logo=team_logo, team_status=team_status, team_user_id=team_user_id, team_passwd=team_passwd)

                qry.save()

                succ_msg = "Team Registered Succesfully"

                return render(request, 'Common/TeamRegistration.html', {'form': form, 'types': sport_types, 'succ_msg': succ_msg})
            else:
                err_msg = "Email Already Exist"
                return render(request, 'Common/TeamRegistration.html', {'form': form, 'types': sport_types, 'err_msg': err_msg})

    return render(request, 'Common/TeamRegistration.html', {'form': form, 'types': sport_types})


def VenueReg(request):
    form = VenueRegForm()
    if request.method == 'POST':
        form = VenueRegForm(request.POST, request.FILES)
        if form.is_valid():
            venue_name = form.cleaned_data['venue_name'].lower()
            venue_type = form.cleaned_data['venue_type']
            venue_address = form.cleaned_data['venue_address'].lower()
            venue_contact = form.cleaned_data['venue_contact']
            venue_email = form.cleaned_data['venue_email']
            venue_pic = form.cleaned_data['venue_pic']
            venue_seat = form.cleaned_data['venue_seat']
            venue_passwd = get_random_string(length=8)
            venue_status = "not approved"
            enc_passwd = pbkdf2_sha256.hash(
                venue_passwd, rounds=1000, salt_size=32)
            venue_id = GetvenueID()

            do_exist = VenueDetails.objects.filter(
                venue_email=venue_email).exists()

            if do_exist:
                msg = "Venue Already Added"
                return render(request, 'Common/VenueRegister.html', {'form': form, 'msg': msg})
            else:

                qry = VenueDetails(venue_name=venue_name, venue_type=venue_type, venue_address=venue_address, venue_contact=venue_contact, venue_email=venue_email,
                                   venue_user_id=venue_id, venue_pic=venue_pic, venue_seat=venue_seat, venue_passwd=enc_passwd, venue_status=venue_status)

                qry.save()

                msg = "Venue Registered Succesfully"
                form = VenueRegForm()
                return render(request, 'Common/VenueRegister.html', {'form': form, 'msg': msg})
        else:
            print(form.errors)
    return render(request, 'Common/VenueRegister.html', {'form': form, })


def MemberReg(request):
    if request.method == 'POST':

        m_name = request.POST['m_name'].lower()
        m_email = request.POST['m_email'].lower()
        m_phno = request.POST['m_phno']
        m_passwd = request.POST['m_passwd']

        enc_passwd = pbkdf2_sha256.hash(m_passwd, rounds=1000, salt_size=32)
        do_exist = MemberDetails.objects.filter(m_email=m_email).exists()

        if not do_exist:
            member = MemberDetails(
                m_name=m_name, m_email=m_email, m_phno=m_phno, m_passwd=enc_passwd)
            member.save()
            succ_msg = "Registered Succesfully"
            return render(request, 'Common/MemberReg.html', {'succ_msg': succ_msg})
        else:
            err_msg = "Email Aleady Exist"
            return render(request, 'Common/MemberReg.html', {'err_msg': err_msg})
    return render(request, 'Common/MemberReg.html')
