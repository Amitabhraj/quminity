from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from Qapp.models import CustomUser as User

def MainView(request, studentId, qid, studentName):
    print(f"Received parameters - studentId: {studentId}, qid: {qid}, studentName: {studentName}")
    try:
        student_obj = User.objects.get(
            id=studentId,
            qid=qid, 
            username=studentName
        )
    except User.DoesNotExist:
        messages.error(request, "User account not found or invalid credentials.")
        return redirect(reverse('user_login')) 
    
    # Context variable is automatically passed to the template for use
    context = {
        'student_user': student_obj,
    }
    
    return render(request, 'html/dashboard/index.html', context)