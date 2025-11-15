from django.contrib.auth.models import *
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout


#################################################
########### Logout Start ####################
#################################################

def user_logout(request,userId):
    if request.user.is_authenticated:
        user_id = request.user.id
        if user_id == userId:
            logout(request)
            messages.success(request, "Successfully Logged Out")
            return redirect("/")
        else:
            messages.error(request, "Invalid Action")
            return redirect("/")

#################################################
########### Logout END ####################