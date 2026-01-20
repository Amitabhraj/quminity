from django.shortcuts import redirect, render
from Qapp.decorators import login_required
from Qapp.models import ClubPayment
from Qapp.use_cases.club.getClub import GetClub
from Qapp.use_cases.payment.CreatePayment import CreatePayment
from Qapp.use_cases.payment.paymentStatus import checkPaymentExist

@login_required
def CreateClubPayment(request, clubId):
    payment_exist = checkPaymentExist(request,clubId,eventId=None)
    club = GetClub(clubId) #if club['redirect']==True , it means That club does exist of Provided Club-ID 

    if club['redirect'] or payment_exist:
        return redirect('ClubEventList')
    
    payment = CreatePayment(request,clubId=clubId,eventId=None)

    return render(request, "html/dashboard/payment.html", context=payment)