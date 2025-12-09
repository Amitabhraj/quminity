from django.shortcuts import redirect, render
from Qapp.decorators import login_required
from Qapp.models import ClubPayment, EventPayment
from Qapp.use_cases.club.getClub import GetClub
from Qapp.use_cases.event.getEvent import GetEvent
from Qapp.use_cases.payment.mainPayment import CreatePayment

@login_required
def CreateEventPayment(request, eventId):
    user_obj = request.user

    event = GetEvent(eventId)
    event_obj = event['eventObj']
    if event['redirect']:
        return redirect('/')
    
    try:
        # Check If Payment Already exists
        payment = EventPayment.objects.get(student=user_obj, event=event_obj, status=True)
        return redirect('studentClub',user_obj.id,user_obj.qid,user_obj.username)
    except ClubPayment.DoesNotExist:
        # Create Payment Because User has not Paid for this Club
        payment = CreatePayment(request,clubId=None.id,eventId=event_obj.id)

    return render(request, "html/dashboard/payment.html", context=payment)