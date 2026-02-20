from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone
from Qapp.decorators import is_associatedWithEvent
from Qapp.decorators import is_associatedWithEvent
from Qapp.models import Attendance, Event


@is_associatedWithEvent
def ListAssociatedEvent(request):
    associated_event = Event.objects.get_associated_events(request.user)
    context = {
        'associated_event': associated_event
    }
    return render(request, 'html/ClubEvent/event/ShowAssociatedEvent.html', context)    