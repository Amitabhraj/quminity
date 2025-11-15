from pyexpat.errors import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import login, authenticate, logout
from flask import redirect


def MainView(request,adminId,adminName):
    return render(request, 'main_education/moderator_side/moderator_dashboard.html') 