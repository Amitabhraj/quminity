from django.shortcuts import render
from Qapp.decorators import faculty_required

@faculty_required
def MainView(request):
    return render(request, 'html/dashboard/faculty_dashboard.html')