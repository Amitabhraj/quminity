from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from Qapp.decorators import login_required
from Qapp.models import CustomUser, Event


@login_required
def GenerateCertificate(request, eventId):
    if request.method != 'POST':
        return HttpResponse('Invalid request')


    student_ids = request.POST.getlist('students')
    event = Event.objects.get(id=eventId)

    for student_id in student_ids:
        student = CustomUser.objects.get(id=student_id)

        # --- SIMPLE CERTIFICATE (HTML → PDF recommended later) ---
        subject = f"Certificate of Participation - {event.event}"
        message = f"""
        Dear {student.first_name},


        Congratulations 🎉
        This is to certify that you have successfully participated in the event:
        EVENT: {event.event}
        DATE: {event.event_date.strftime('%d %B %Y')}
        Regards,
        Quminity Team
        """


        email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [student.email]
        )
        # email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=True)


    return redirect('ManageEvent', eventId=event.id)