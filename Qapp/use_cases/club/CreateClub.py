from django.shortcuts import render
from Qapp.decorators import moderator_required


@moderator_required
def CreateClub(request):
    return render(request, "html/ClubEvent/club/create-club.html")
