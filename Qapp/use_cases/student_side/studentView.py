from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from Qapp.models import CustomUser as User
from Qapp.use_cases.student_side.check_student_cred import check_cred

def MainView(request, studentId, qid, studentName):
    student_obj = check_cred(request, studentId, qid, studentName) 
    
    # Context variable is automatically passed to the template for use
    context = {
        'student_user': student_obj,
    }
    
    return render(request, 'html/dashboard/index.html', context)