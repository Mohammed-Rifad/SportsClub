from ClubManagementApp.views import VenueView
from django.urls import path
from  .views import CommonView,AdminView,UsersView,PlayersView,TeamView

app_name="club_management"


urlpatterns=[
    path('',CommonView.ProjectHome,name="home"),
    path('AdminData',CommonView.AdminData),
    path('Admin/PendingTeam',AdminView.PendingTeamRequest,name="team_request"),
    path('Admin/PendingVenue',AdminView.PendingVenueRequest,name="venue_request"),
    path('Admin/AddTournament',AdminView.AddTournament,name="add_tournament"),
    path('AdminHome/ViewBlock/<int:venue_id>',AdminView.ViewBlock,name="view_block"),
    path('AdminHome/GetVenue',AdminView.getVenue,name="get_venue"),
    path('AdminHome/ViewPlayers/<int:team_id>',AdminView.ViewPlayers,name="view_players"),
    path('Admin/ViewTeams',AdminView.ViewTeams,name="view_teams"),
    path('Admin/ViewVenue',AdminView.ViewVenue,name="view_venue"),
    path('Admin/ApproveTeam/<int:id>',AdminView.ApproveTeam,name="approve_team"),
    path('Admin/RejectTeam/<int:id>',AdminView.RejectTeam,name="reject_team"),
    path('Admin/TournamentRequest',AdminView.TournamentRequest,name="t_request"),
    path('Admin/ApproveVenue/<int:id>',AdminView.ApproveVenue,name="approve_venue"),
    path('Admin/RejectVenue/<int:id>',AdminView.RejectVenue,name="reject_venue"),
    path('Login',CommonView.Login,name="login"),
    path('AdminHome',AdminView.AdminHome,name="admin_home"),
    path('AdminHome/AddSports',AdminView.AddSport,name="add_sport"),
    path('AdminHome/Notification',AdminView.AddNotification,name="add_notification"),
    path('TeamReg',CommonView.TeamReg,name="team_reg"),
    path('PlayerHome',PlayersView.PlayerHome,name="player_home"),
    path('TeamHome',TeamView.TeamHome,name="team_home"),
    path('TeamHome/ViewPlayers',TeamView.ViewPlayers,name="view_players"),
    path('TeamHome/Tournaments',TeamView.ViewTournaments,name="ta_view_tournaments"),
    path('TeamHome/T-Players/<int:id>',TeamView.AddTournamentPlayers,name="t_players"),
    path('TeamHome/Edit/<int:id>',TeamView.EditPlayer,name="edit_player"),
    path('TeamHome/Del/<int:id>',TeamView.DeletePlayer,name="delete_player"),
    path('TeamHome/View/<int:id>',TeamView.ViewPlayer,name="view_player"),
    path('TeamHome/Logout',TeamView.Logout,name="logout"),
    path('Team/AddPlayer',TeamView.AddPlayer,name='add_player'),
    path('RegisterVenue',CommonView.VenueReg,name="venue_reg"),
    path('VenueHome',VenueView.VenueHome,name="venue_home"),
    path('VenueHome/AddBlock',VenueView.AddBlock,name="add_block")
]