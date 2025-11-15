from Qapp.models import CustomUser as User
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

def check_cred(request,studentId, qid, studentName):
    try:
        student_obj = User.objects.get(
            id=studentId,
            qid=qid, 
            username=studentName
        )
    except User.DoesNotExist:
        messages.error(request, "User account not found or invalid credentials.")
        return redirect(reverse('user_login'))
    
    return student_obj