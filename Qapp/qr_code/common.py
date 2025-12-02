from Qapp.models import Club

def get_event_or_club_association_from_user(request):
    usr_obj = request.user
    event_or_club = Club.objects.filter(core_members=usr_obj)

    if not event_or_club.exists():
        return False, "User is not associated with any club"

    return True, event_or_club



def check_club_core_member(request,club_id):
    usr_obj = request.user
    try:
        event_or_club = Club.objects.get(id=club_id,core_members=usr_obj)
    except Club.DoesNotExist:
        return False, "Club Does not Exists or Core Member is not associated with this club"
    
    return True, event_or_club