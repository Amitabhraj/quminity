from Qapp.decorators import login_required
from Qapp.models import Club, CustomUser


def GetClub(clubId):
    try:
        club = Club.objects.get(id=clubId)
        return {'redirect':False,'clubObj':club}
    except:
        return {'redirect':True,'clubObj':None}
    

def getActiveClubList():
    club = Club.objects.filter(active=True)
    return club


def getAssociatedClubList(user):
    associated_club_list = []
    if user.is_authenticated:
        associated_club_list = user.faculty_assigned_club.filter(active=True)
    return associated_club_list