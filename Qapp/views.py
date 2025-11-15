from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import CustomUser as User

# Create your views here.
def check_authentication(request):
    user_obj = request.user
    if not user_obj.is_authenticated:
        return redirect("/login")
    else:
        input_user_type = user_obj.groups.first().name if user_obj.groups.exists() else None
        if input_user_type == "Admin":
            return redirect('adminView', adminId=user_obj.qid,qid=user_obj.qid , adminName=user_obj.username)
        elif input_user_type == "Faculty":
            return redirect('facultyView', facultyId=user_obj.id,qid=user_obj.qid , facultyName=user_obj.username)
        elif input_user_type == "Student":
            return redirect('studentView', studentId=user_obj.id, qid=user_obj.qid ,studentName=user_obj.username)
        else:
            messages.error(request, "Authentication failed.")
            return redirect("/login")