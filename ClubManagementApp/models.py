from pyexpat import model
from django.db import models
from passlib.hash import pbkdf2_sha256
# Create your models here.



class AdminDetails(models.Model):
    login_id=models.CharField(max_length=20,db_column="log_id")
    login_passwd=models.CharField(max_length=120,db_column='passwd')

    class Meta:
        db_table="tb_super"

    def verifyPasswd(self,raw_passwd):
        return pbkdf2_sha256.verify(raw_passwd,self.login_passwd)




class SportsDetail(models.Model):
    Sport_Choices=(
        ('m','Men'),
        ('w','Women')
    )
    sport_id=models.AutoField(primary_key=True,db_column="sp_id")
    sport_name=models.CharField(max_length=50,db_column="sp_name")
    sport_type=models.CharField(max_length=10,db_column="sp_type",choices=Sport_Choices)
    class Meta:
        db_table="tb_sports"

class TeamDetails(models.Model):
    team_id=models.AutoField(primary_key=True,db_column="t_id")
    team_type=models.ForeignKey(SportsDetail,on_delete=models.CASCADE,db_column="t_type")
    team_name=models.CharField(max_length=50,db_column="t_name")
    team_place=models.CharField(max_length=50,db_column="t_place")
    team_email=models.EmailField(max_length=100,db_column="tb_mail")
    team_phno=models.CharField(max_length=10,db_column="t_ph")
    team_user_id=models.IntegerField()
    team_logo=models.ImageField(upload_to="Team/",db_column="t_logo")
    team_passwd=models.CharField(max_length=120,db_column="t_pswd")
    team_status=models.CharField(max_length=20,db_column="t_status")

    class Meta:
        db_table="tb_team"
        
    def verifyPasswd(self,raw_passwd):
        return pbkdf2_sha256.verify(raw_passwd,self.team_passwd)

class PlayerDetails(models.Model):
    player_id=models.AutoField(primary_key=True,db_column="p_id")
    team_id=models.ForeignKey(TeamDetails,on_delete=models.CASCADE,db_column="t_id")
    player_name=models.CharField(max_length=20,db_column="p_name")
    player_position=models.CharField(max_length=20,db_column="p_pos")
    player_address=models.CharField(max_length=200,db_column="p_addr")
    player_dob=models.CharField(max_length=20,db_column="p_dob")
    player_email=models.EmailField(db_column="p_email")
    player_img=models.ImageField(upload_to="Player/",db_column="p_img")
    player_height=models.IntegerField(db_column="p_height",default=0)
    player_weight=models.IntegerField(db_column="p_weight",default=0)
    player_ph=models.CharField(max_length=10,db_column="p_ph")
    player_passwd=models.CharField(max_length=120,db_column="p_pswd")
    class Meta:
        db_table="tb_players"
    
    def verifyPasswd(self,raw_passwd):
        return pbkdf2_sha256.verify(raw_passwd,self.player_passwd)

class AdminNotification(models.Model):
    notfn_id=models.AutoField(primary_key=True,db_column="notfn_id")
    notfn_date=models.CharField(max_length=20,default="", db_column="notfn_date")
    notfn_title=models.CharField(max_length=120,db_column="notfn_title",default="")
    notfn_content=models.CharField(max_length=255,db_column="notfn_content")

    class Meta:
        db_table="tb_notfn"


class VenueDetails(models.Model):
    venue_id=models.AutoField(primary_key=True,db_column="v_id")
    venue_name=models.CharField(max_length=30,db_column="v_name")
    venue_type=models.CharField(max_length=20,db_column="v_type")
    venue_address=models.CharField(max_length=200,db_column="v_address")
    venue_contact=models.CharField(max_length=10,db_column="v_contact")
    venue_email=models.CharField(max_length=30,db_column="v_email")
    venue_user_id=models.IntegerField(db_column="v_userid")
    venue_pic=models.ImageField(upload_to="Venue/",db_column="v_pic")
    venue_seat=models.ImageField(upload_to="Venue/Seat/",db_column="v_seat")
    venue_passwd=models.CharField(max_length=20,db_column="v_passwd")
    venue_status=models.CharField(max_length=10,db_column="v_status")
    class Meta:
        db_table="tb_venue"

    def verifyPasswd(self,raw_passwd):
        return pbkdf2_sha256.verify(raw_passwd,self.venue_passwd)
        
class BlockDetails(models.Model):
    venue_id=models.ForeignKey(VenueDetails,on_delete=models.CASCADE,db_column="v_id")
    block_title=models.CharField(max_length=20,db_column="b_title")
    amount=models.FloatField(db_column="amt")
    total_seats=models.IntegerField(db_column="seats")
    class Meta:
        db_table="tb_block"


class TournamentDetails(models.Model):
    tournament_id=models.AutoField(primary_key=True,db_column="t_id")
    venue_id=models.ForeignKey(VenueDetails,on_delete=models.SET_NULL,null=True,db_column="v_id")
    tournament_title=models.CharField(max_length=20,db_column="t_title")
    sport_type=models.ForeignKey(SportsDetail,on_delete=models.CASCADE,db_column="s_type")
    players_allowed=models.IntegerField(db_column='max_players')
    start_date=models.CharField(max_length=20,db_column="s_date")
    end_date=models.CharField(max_length=20,db_column="e_date")
    reg_date=models.CharField(max_length=20,db_column="reg_date")
    reg_fee=models.FloatField(db_column="reg_fee")
    win_prize=models.FloatField(db_column="win_prize")
    winner=models.ForeignKey(TeamDetails,on_delete=models.CASCADE,null=True)
    tournament_status=models.CharField(max_length=20,db_column="t_status")
    
    class Meta:
        db_table="tb_tournament"


class TournamentRegistration(models.Model):
    tournament_id=models.ForeignKey(TournamentDetails,on_delete=models.SET_NULL,null=True)
    team_id=models.ForeignKey(TeamDetails,on_delete=models.CASCADE,default="")
    team_status=models.CharField(max_length=20,default='not approved')
    team_point=models.IntegerField(default=0)
    
    class Meta:
        db_table="tb_tournamentReg"


class TournamentPlayers(models.Model):
    tournament_id=models.ForeignKey(TournamentDetails,on_delete=models.SET_NULL,null=True)
    player_id=models.ForeignKey(PlayerDetails,on_delete=models.CASCADE)
    team_id=models.ForeignKey(TeamDetails,on_delete=models.CASCADE,default="")
    cert=models.FileField(upload_to="",default="Players/Certificates")
    player_status=models.CharField(max_length=20,default='not approved')
    
    
    class Meta:
        db_table="tb_tournamentPlayers"


class Fixture(models.Model):
    tournament_id=models.ForeignKey(TournamentDetails,on_delete=models.CASCADE)
    team1=models.ForeignKey(TeamDetails,on_delete=models.CASCADE,related_name='team1',null=True)
    team2=models.ForeignKey(TeamDetails,on_delete=models.CASCADE,related_name='team2',null=True)
    match=models.CharField(max_length=50)
    date=models.CharField(max_length=20)
    time=models.CharField(max_length=20)
    team1_score=models.CharField(max_length=10)
    team2_score=models.CharField(max_length=10)
    result=models.CharField(max_length=30)  
    match_video=models.FileField('video/',default="")
    class Meta:
        db_table="tb_fixture"