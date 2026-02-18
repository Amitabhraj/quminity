from django.shortcuts import render
from Qapp.decorators import login_required
from Qapp.use_cases.event.getEvent import getActiveEventList

@login_required
def EventList(request):
    event = getActiveEventList()

    context = {
        'events':event
    }

    return render(request,'html/ClubEvent/event/listEvent.html',context)