from django.http import JsonResponse
from django.shortcuts import render,redirect
from Qapp.decorators import login_required
from Qapp.qr_code.common import check_club_core_member, get_event_or_club_association_from_user


@login_required
def ShowAssociatedClub(request):
    success, result = get_event_or_club_association_from_user(request)
    if not success:
        return redirect("/")
    context = {'club': result}
    return render(request, "html/QrCode/ShowAssociatedClub.html", context)



def QrGeneratePage(request,club_id):
    success, club_or_event = check_club_core_member(request,club_id)
    if not success:
        return redirect("/")
    context = {'club':club_or_event}
    return render(request, "html/QrCode/GenerateQR.html",context)


def scan_page(request):
    return render(request, "html/QrCode/studentScan.html")