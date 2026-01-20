from django.shortcuts import render
from Qapp.decorators import login_required
from Qapp.use_cases.club.getClub import getClubList
from Qapp.use_cases.event.getEvent import getEventList

@login_required
def ClubEventList(request):
    club = getClubList()
    event = getEventList()

    context = {
        'clubs':club,
        'events':event
    }

    return render(request,'html/ClubEvent/ListClubEvent.html',context)