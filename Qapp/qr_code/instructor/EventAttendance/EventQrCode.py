from django.shortcuts import render,redirect
from Qapp.decorators import login_required
from Qapp.use_cases.event.getEvent_coordinator import check_event_coordinator

@login_required
def QrGeneratePage(request,eventId):
    event = check_event_coordinator(request,eventId)
    if not event:
        return redirect("/")
    context = {'event':event}
    return render(request, "html/QrCode/GenerateAttendanceQR.html",context)
