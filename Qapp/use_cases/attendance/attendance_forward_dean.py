def ForwardAttendanceToDean(request,eventId):
    from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.shortcuts import redirect
from Qapp.models import Event, Attendance


@login_required
def ForwardAttendanceToDean(request, eventId):
    if request.method != "POST":
        return redirect('ManageEvent', eventId=eventId)
    
    event = Event.objects.get(id=eventId)

    attendance = Attendance.objects.filter(event=eventId).select_related('student').order_by('student__qid')

    present = attendance.filter(is_present=True)
    absent = attendance.filter(is_present=False)

    # 🔹 Build Email Content
    subject = f"Attendance Report: {event.event}"

    text_message = f"""
    Attendance Report

    Event: {event.event}
    Date: {event.event_date.strftime('%d %B %Y')}
    Location: {event.location}

    Total Students: {attendance.count()}
    Present: {present.count()}
    Absent: {absent.count()}
    """

    return redirect('manage_event', event_id=event.id)
