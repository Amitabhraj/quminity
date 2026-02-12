from django.shortcuts import render
from Qapp.decorators import login_required,moderator_required

@login_required
@moderator_required
def MainView(request):
    return render(request, 'html/dashboard/moderator_dashboard.html') 