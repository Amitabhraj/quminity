from django.contrib.auth.models import *
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout


#################################################
########### Logout Start ####################
#################################################

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Successfully Logged Out")
        return redirect("/")
    else:
        messages.error(request, "No user is logged in")
        return redirect("/")

#################################################
########### Logout END ####################