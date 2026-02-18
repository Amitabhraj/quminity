from django.shortcuts import render
from Qapp.decorators import login_required
from Qapp.use_cases.club.getClub import getActiveClubList

@login_required
def ClubList(request):
    club = getActiveClubList()

    context = {
        'clubs':club
    }

    return render(request,'html/ClubEvent/club/listClub.html',context)