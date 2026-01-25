from django.shortcuts import redirect
from django.contrib.auth import logout

def handle_404_redirect(request, exception=None):
    if request.user.is_authenticated:
        if request.user.user_type == "Student":
            return redirect('studentView')
        elif request.user.user_type == "Faculty":
            return redirect('facultyView')
        elif request.user.user_type == "Admin":
            return redirect('adminView')
        elif request.user.user_type == "Dean":
            return redirect('DeanView')
        else:
            logout(request)
            return redirect('user_login')
    else:
        # If not logged in, send them to the login page
        return redirect('user_login') # Replace 'login' with your login URL name