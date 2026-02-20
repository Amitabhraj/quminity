from django.http import Http404
from django.shortcuts import get_object_or_404, render
from Qapp.decorators import login_required
from Qapp.models import Event

@login_required
def QrGeneratePage(request,EventId):
    if not Event.objects.is_user_associated_with_provided_event(request.user, EventId):
        raise Http404

    event_instance = get_object_or_404(Event, id=EventId)
    context = {
        'event': event_instance
    }
    return render(request, "html/QrCode/GenerateAttendanceQR.html",context)
