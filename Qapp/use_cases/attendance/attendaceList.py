from django.shortcuts import render
from Qapp.decorators import login_required
from Qapp.models import Attendance, Event

@login_required
def ListEventAttendace(request,eventId):
    event = Event.objects.get(id=eventId)
    attendance = Attendance.objects.filter(event=event,is_present=True)
    context = {
        'event':event,
        'attendance':attendance
    }
    return render(request,'html/attendance/attendancelist.html', context)