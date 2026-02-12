from django.shortcuts import render
from Qapp.decorators import student_required
from Qapp.qr_code.common import get_event_or_club_association_from_user
from Qapp.use_cases.student_side.check_student_cred import check_cred

@student_required
def MainView(request):
    student_user = request.user
    response = get_event_or_club_association_from_user(request)

    # Context variable is automatically passed to the template for use
    context = {
        'student_user':student_user,
        'club': response['redirect'],
    }
    
    return render(request, 'html/dashboard/student_dashboard.html', context)