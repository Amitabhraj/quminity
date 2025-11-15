"""
URL configuration for quminity project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.contrib import admin
from django.urls import include, path
from .views import *
from .use_cases.user_onboarding.logout_user import user_logout
from .use_cases.user_onboarding.user_login import user_login
from .use_cases.student_side.studentView import MainView as student_dashboard
from .use_cases.faculty_side.facultyView import MainView as faculty_dashboard
from .use_cases.admin_side.adminView import MainView as admin_dashboard

urlpatterns = [
    path('', check_authentication, name='check_authentication'),
    path('login/', user_login, name='user_login'),
    path('logout_user/<int:userId>/', user_logout, name='user_logout'),
    path('student_dashboard/<int:studentId>/<str:studentName>/', student_dashboard, name='student_dashboard'),
    path('teacher_dashboard/<int:facultyId>/<str:facultyName>/', faculty_dashboard, name='faculty_dashboard'),
    path('moderator_dashboard/<int:adminId>/<str:adminName>/', admin_dashboard, name='admin_dashboard'),
]




