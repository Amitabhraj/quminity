# views.py
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from Qapp.decorators import login_required
from Qapp.models import Attendance, ClassRoom, Event, Notification


@login_required
def ApproveEventAttendance(request, eventId):
    event = get_object_or_404(Event, id=eventId)
    attendance = Attendance.objects.filter(event=event,is_present=True)
    for attendance in attendance:
        student = attendance.student
        classroom = ClassRoom.objects.filter(student=student,present=False)
        for classroom in classroom:
            classroom.present = True
            classroom.save()
    messages.success(
        request,
        f"Attendance for '{event.event}' approved successfully."
    )
    return redirect('DeanDashboard')
