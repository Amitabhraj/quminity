from pyexpat.errors import messages
from django.shortcuts import render
from flask import redirect
from django.contrib.auth import authenticate, login
from Qapp.models import CustomUser as User

# Create your views here.
def user_login(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        qid = request.POST.get("qid", "").strip()
        password = request.POST.get("password", "").strip()

        # Validate user existence
        try:
            user_obj = User.objects.get(qid=qid)
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect("/")  # Redirect after message

        # Check password
        if not user_obj.check_password(password):
            messages.error(request, "Incorrect password.")
            return redirect("/")
        
        input_user_type = user_obj.groups.first().name if user_obj.groups.exists() else None

        # Authenticate and login
        user = authenticate(username=user_obj.username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Successfully logged in!")
            
            if input_user_type == "Admin":
                return redirect('adminView', adminId=user_obj.qid, adminName=user_obj.username)
            elif input_user_type == "Teacher":
                return redirect('facultyView', FacultyId=user_obj.id, facultyName=user_obj.username)
            elif input_user_type == "Student":
                return redirect('studentView', studentId=user_obj.id, studentName=user_obj.username)
            else:
                messages.error(request, "Authentication failed.")
                return redirect("/")
        else:
            messages.error(request, "Authentication failed.")
            return redirect("/")
        
    return render(request, 'html/dashboard/sign-in.html')  