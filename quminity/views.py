from django.shortcuts import redirect, render

def handle_404_redirect(request, exception):
    if request.path == "/":
        if request.user.is_authenticated:
            user_type = request.user.user_type
            if user_type == 'Student':
                return redirect('studentView')
            elif user_type == 'Faculty':
                return redirect('facultyView')
            elif user_type == 'Dean':
                return redirect('DeanView')
            elif user_type == 'Admin':
                return redirect('adminView')
        else:
            return redirect('user_login')
        
    return render(request, 'html/404.html', status=404)
