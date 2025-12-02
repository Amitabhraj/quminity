from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from Qapp.models import CustomUser as User
from Qapp.qr_code.common import get_event_or_club_association_from_user
from Qapp.use_cases.student_side.check_student_cred import check_cred

def MainView(request, studentId, qid, studentName):
    student_user = check_cred(request, studentId, qid, studentName)
    success, result = get_event_or_club_association_from_user(request)
    if not success:
        return redirect("/")
    
    # Context variable is automatically passed to the template for use
    context = {
        'student_user':student_user,
        'club': result,
    }
    
    return render(request, 'html/dashboard/index.html', context)