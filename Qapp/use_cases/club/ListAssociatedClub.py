from django.shortcuts import render
from Qapp.decorators import is_associatedWithClub
from Qapp.models import Club


@is_associatedWithClub
def ListAssociatedClub(request):
    associated_club = Club.objects.get_associated_clubs(request.user)
    context = {
        'associated_club': associated_club
    }
    return render(request, "html/ClubEvent/club/ShowAssociatedClub.html", context)
