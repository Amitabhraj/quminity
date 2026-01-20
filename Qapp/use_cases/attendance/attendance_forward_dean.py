from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.utils import timezone
from Qapp.models import Event, Attendance, Notification, CustomUser


@login_required
def ForwardAttendanceNotificationToDean(request, eventId):
    if request.method != "POST":
        return redirect('ManageEvent', eventId=eventId)

    event = get_object_or_404(Event, id=eventId)

    #Get Dean group
    try:
        dean_group = Group.objects.get(name="Dean")
    except Group.DoesNotExist:
        messages.error(request, "Dean group Does not Exists")
        return redirect('ManageEvent', eventId=event.id)

    # Get all deans
    deans = CustomUser.objects.filter(groups=dean_group)

    if not deans.exists():
        messages.error(request, "No users assigned to Dean group")
        return redirect('ManageEvent', eventId=event.id)

    attendance_qs = Attendance.objects.filter(event=event)
    present_count = attendance_qs.filter(is_present=True).count()

    message = f"""
            Attendance for the event '{event.event}' has been forwarded.
            Event Date: {event.event_date.strftime('%d %B %Y')}
            Location: {event.location}
            Total Present Student: {present_count}
            Forwarded by: {request.user.username}
            """

    # Create notification for each dean
    for dean in deans:
        Notification.objects.create(
            push_to=dean,
            event=event,
            notificatio_type="Marking Attendance",
            push_by = request.user,
            subject = f"Attendance Forwarded for Event - {event.event}",
            message= message,
            date = timezone.now()
        )
    messages.success(request, "Attendance has been forwarded to the Dean successfully.")
    return redirect('ManageEvent', eventId=event.id)
