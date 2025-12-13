from django.shortcuts import render
from Qapp.decorators import login_required
from Qapp.models import Attendance

@login_required
def ListEventAttendace(request,eventId):
    event = Event.objects.get(id=eventId)
    attendance = Attendance.objects.filter(event=event,present=True)
    context = {
        'attendance':attendance
    }
    return render(request,'html/dashboard/dean_dashboard.html', context)