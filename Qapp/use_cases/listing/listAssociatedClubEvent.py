from django.shortcuts import redirect, render
from Qapp.decorators import login_required
from Qapp.qr_code.common import get_user_associations


@login_required
def ShowAssociatedClub(request):
    response = get_user_associations(request)
    if response['redirect']:
        return redirect("/")
    return render(request, "html/ClubEvent/ShowAssociatedClub.html", response)
