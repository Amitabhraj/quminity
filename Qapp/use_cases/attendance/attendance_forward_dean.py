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

    # 🔹 HTML Message (Professional)
    html_message = f"""
    <h3>Attendance Report</h3>
    <p><strong>Event:</strong> {event.event}</p>
    <p><strong>Date:</strong> {event.event_date.strftime('%d %B %Y')}</p>
    <p><strong>Location:</strong> {event.location}</p>

    <hr>

    <p><strong>Total Students:</strong> {attendance.count()}</p>
    <p style="color:green;"><strong>Present:</strong> {present.count()}</p>
    <p style="color:red;"><strong>Absent:</strong> {absent.count()}</p>

    <h4>Student List</h4>
    <table border="1" cellpadding="6" cellspacing="0">
      <tr>
        <th>Name</th>
        <th>Status</th>
        <th>Marked At</th>
      </tr>
    """

    for att in attendance:
        html_message += f"""
        <tr>
          <td>{att.student}</td>
          <td>{"Present" if att.is_present else "Absent"}</td>
          <td>{att.attendance_marked_at.strftime('%d %b %Y, %I:%M %p')}</td>
        </tr>
        """

    html_message += "</table><br><p>Regards,<br>Quminity System</p>"

    # 🔹 Dean Email (CHANGE THIS)
    dean_email = "dean@quminity.com"

    email = EmailMultiAlternatives(
        subject,
        text_message,
        settings.DEFAULT_FROM_EMAIL,
        [dean_email]
    )
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)

    return redirect('manage_event', event_id=event.id)
