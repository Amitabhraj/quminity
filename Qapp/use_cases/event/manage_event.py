from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def ManageEvent(request):
    return render(request, 'html/ClubEvent/event/manage-event.html')    