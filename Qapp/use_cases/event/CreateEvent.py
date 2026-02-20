from django.shortcuts import render
from Qapp.decorators import is_associatedWithClub
from Qapp.models import Club


@is_associatedWithClub
def CreateEvent(request):
    associated_club = Club.objects.get_associated_clubs(request.user)
    context = {
        'clubs': associated_club
    }
    return render(request, "html/ClubEvent/event/create-event.html", context)
