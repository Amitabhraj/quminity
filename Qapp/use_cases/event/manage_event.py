from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone
from Qapp.models import Attendance, Event


@login_required
def manageEvent(request, eventId):
    event = get_object_or_404(Event, id=eventId)

    # Permission check
    if not (
        request.user in event.faculty_assigned.all() or
        request.user in event.event_coordinator.all()
        ):
        return HttpResponseForbidden("You are not allowed to manage this event")


    if request.method == 'POST':
        event.event = request.POST.get('event')
        event.event_date = request.POST.get('event_date')
        event.location = request.POST.get('location')
        event.entry_fees = request.POST.get('entry_fees')
        event.description = request.POST.get('description')
        event.updated_at = timezone.now()
        event.save()


        return redirect('ManageEvent', eventId=event.id)


    attendance = Attendance.objects.filter(event=event).select_related('student')


    context = {
    'event': event,
    'attendance': attendance
    }
    return render(request, 'html/ClubEvent/event/manage-event.html', context)    