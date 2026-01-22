from Qapp.models import Club, Event
from django.db.models import Q

def get_event_or_club_association_from_user(request):
    usr_obj = request.user
    redirect = False
    event = Event.objects.filter(Q(faculty_assigned=usr_obj) | Q(event_coordinator=usr_obj)).distinct()
    club = Club.objects.filter(core_members=usr_obj)

    if not event and not club:
        redirect = True

    context = {
        'events':event,
        'clubs':club,
        'redirect':redirect
    }
    return context



def check_club_core_member(request,club_id):
    usr_obj = request.user
    try:
        event_or_club = Club.objects.get(id=club_id,core_members=usr_obj)
    except Club.DoesNotExist:
        return False, "Club Does not Exists or Core Member is not associated with this club"
    
    return True, event_or_club