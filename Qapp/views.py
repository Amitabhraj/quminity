from pyexpat.errors import messages
from django.shortcuts import render
from flask import redirect
from django.contrib.auth import authenticate, login
from .models import CustomUser as User

# Create your views here.
def check_authentication(request):
    return redirect("/login")