from django.http import JsonResponse
from django.shortcuts import render
from Qapp.decorators import login_required
from Qapp.models import Club, ClubPayment, CustomUser, Event, EventPayment
from Qapp.use_cases.payment.GetPayment_orderID import GetPayment

"""
This Function Return ***FINAL PAYMENT STATUS*** (if the Payment is Successfull or not)
"""

@login_required
def PaymentStatus(request, order_id):
    get_payment = GetPayment(request,order_id) # Get Payment Details with Order-id from Database for Verification
    payment_obj = get_payment['payment'] # Payment Object

    if get_payment['redirect']:
        return JsonResponse({"message":get_payment['message']})
    
    return render(request,"html/dashboard/paymentStatus.html",{"payment":payment_obj})



def checkPaymentExist(request,clubId,eventId):
    usr_obj = CustomUser.objects.get(id=request.user.id)
    if clubId:
        try:
            club_obj = Club.objects.get(id=clubId)
            payment = ClubPayment.objects.get(student=usr_obj,club=club_obj,status=True)
        except:
            payment = False
    elif eventId:
        try:
            event_obj = Event.objects.get(id=eventId)
            payment = EventPayment.objects.get(student=usr_obj,event=event_obj,status=True)
        except:
            payment = False
    
    return payment #True ---> Payment Exists , False---> Payment Does not Exists
