from Qapp.decorators import login_required
from Qapp.models import Club, CustomUser


def GetClub(clubId):
    try:
        club = Club.objects.get(id=clubId)
        return {'redirect':False,'clubObj':club}
    except:
        return {'redirect':True,'clubObj':None}
    

def getClubList():
    club = Club.objects.filter(active=True)
    return club