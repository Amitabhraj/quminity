from django.shortcuts import redirect, render
from Qapp.decorators import login_required
from Qapp.models import ClubPayment
from Qapp.use_cases.club.getClub import GetClub
from Qapp.use_cases.payment.mainPayment import CreatePayment

@login_required
def CreateClubPayment(request, clubId):
    user_obj = request.user
    
    club = GetClub(clubId)
    club_obj = club['clubObj']
    if club['redirect']:
        return redirect('/')
    
    try:
        # Check If Payment Already exists
        payment = ClubPayment.objects.get(student=user_obj, club=club_obj, status=True)
        return redirect('studentClub',user_obj.id,user_obj.qid,user_obj.username)
    except ClubPayment.DoesNotExist:
        # Create Payment Because User has not Paid for this Club
        payment = CreatePayment(request,clubId=club_obj.id,eventId=None)

    return render(request, "html/dashboard/payment.html", context=payment)