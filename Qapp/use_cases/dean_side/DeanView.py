from django.shortcuts import render
from Qapp.decorators import login_required
from Qapp.models import Notification

@login_required
def DashboardDean(request):
    dean_user = request.user
    notifications = Notification.objects.filter(push_to=dean_user).order_by('-date')

    # Context variable is automatically passed to the template for use
    context = {
        'dean_user':dean_user,
        'notifications':notifications
    }
    
    return render(request, 'html/dashboard/dean_dashboard.html', context)