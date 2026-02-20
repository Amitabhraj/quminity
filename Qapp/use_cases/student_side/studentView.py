from django.shortcuts import render
from Qapp.decorators import student_required
from Qapp.models import Club, Event

@student_required
def MainView(request):
   context = {
        'is_associated_with_event': Event.objects.get_associated_events(request.user).exists(),
        'is_associated_with_club': Club.objects.get_associated_clubs(request.user).exists(),
    }
   return render(request, 'html/dashboard/student_dashboard.html',context)