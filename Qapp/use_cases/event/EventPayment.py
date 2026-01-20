from django.shortcuts import redirect, render
from Qapp.decorators import login_required
from Qapp.use_cases.event.getEvent import GetEvent
from Qapp.use_cases.payment.CreatePayment import CreatePayment
from Qapp.use_cases.payment.paymentStatus import checkPaymentExist

@login_required
def CreateEventPayment(request, eventId):
    payment_exist = checkPaymentExist(request,clubId=None,eventId=eventId)
    event = GetEvent(eventId) #if club['redirect']==True , it means That club does exist of Provided Club-ID 
    print(payment_exist)
    if event['redirect'] or payment_exist:
        return redirect('ClubEventList')
    
    payment = CreatePayment(request,clubId=None,eventId=eventId)

    return render(request, "html/dashboard/payment.html", context=payment)