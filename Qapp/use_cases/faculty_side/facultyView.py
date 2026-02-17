from django.shortcuts import render
from Qapp.decorators import faculty_required
from Qapp.qr_code.common import get_user_associations

@faculty_required
def MainView(request):
    user = request.user
    response = get_user_associations(user)
    print(response)
    return render(request, 'html/dashboard/faculty_dashboard.html')