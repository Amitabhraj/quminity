from django.shortcuts import redirect, render
from Qapp.common import *

def handle_404_redirect(request, exception):
    if request.path == "/":
        if request.user.is_authenticated:
            user_type = request.user.user_type
            if user_type == student_user:
                return redirect('studentView')
            elif user_type == faculty_user:
                return redirect('facultyView')
            elif user_type == dean_user or user_type == admin_user or user_type == director_user or user_type == vc_user:
                return redirect('adminView')
        else:
            return redirect('user_login')
        
    return render(request, 'html/404.html', status=404)
