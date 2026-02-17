from django.shortcuts import render
from Qapp.decorators import student_required
from Qapp.qr_code.common import get_user_associations

@student_required
def MainView(request):
    user = request.user
    response = get_user_associations(user)
    print(response)
    
    return render(request, 'html/dashboard/student_dashboard.html')