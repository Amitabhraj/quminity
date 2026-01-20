from django.shortcuts import redirect, render
from Qapp.decorators import login_required
from Qapp.qr_code.common import get_event_or_club_association_from_user


@login_required
def ShowAssociatedClub(request):
    response = get_event_or_club_association_from_user(request)
    if response['redirect']:
        return redirect("/")
    return render(request, "html/ClubEvent/ShowAssociatedClub.html", response)
