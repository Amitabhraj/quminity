from functools import wraps
from django.shortcuts import redirect
from django.http import Http404
from Qapp.common import MODERATOR_USER_LIST,student_user,faculty_user

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login/")
        return view_func(request, *args, **kwargs)
    return wrapper

def moderator_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login/")
        if request.user.user_type in MODERATOR_USER_LIST:
            return view_func(request, *args, **kwargs)
        else:
            raise Http404("Page not found") 
    return wrapper


def student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login/")
        if request.user.user_type == student_user:
            return view_func(request, *args, **kwargs)
        else:
            raise Http404("Page not found") 
    return wrapper



def faculty_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login/")
        if request.user.user_type == faculty_user:
            return view_func(request, *args, **kwargs)
        else:
            raise Http404("Page not found") 
    return wrapper