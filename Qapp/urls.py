from django.urls import path
from Qapp.use_cases.payment.user_payment import club_payment, create_payment, payment_done, payment_success
from Qapp.use_cases.student_side.studentClub import studentClub
from Qapp.use_cases.student_side.studentDiscussion import studentDiscussion
from Qapp.use_cases.student_side.studentAcademics import studentAcad
from .views import *
from .use_cases.user_onboarding.logout_user import user_logout
from .use_cases.user_onboarding.user_login import user_login
from .use_cases.student_side.studentView import MainView as student_dashboard
from .use_cases.faculty_side.facultyView import MainView as faculty_dashboard
from .use_cases.admin_side.adminView import MainView as admin_dashboard

urlpatterns = [
    path('', check_authentication, name='check_authentication'),
    path('login/', user_login, name='user_login'),


    path("payment-club/<int:clubId>/<str:clubName>/<int:amount>/", create_payment, name="create_payment"),
    path("payment-success/", payment_success, name="payment_success"),
    path("payment-done/<str:order_id>/", payment_done, name="payment_done"),


    path('logout_user/<int:userId>/', user_logout, name='user_logout'),

    path('studentAcad/<int:studentId>/<int:qid>/<str:studentName>/', studentAcad, name='studentAcad'),
    path('studentClub/<int:studentId>/<int:qid>/<str:studentName>/', studentClub, name='studentClub'),
    path('studentDiscussion/<int:studentId>/<int:qid>/<str:studentName>/', studentDiscussion, name='studentDiscussion'),


    path('student_dashboard/<int:studentId>/<int:qid>/<str:studentName>/', student_dashboard, name='studentView'),
    path('teacher_dashboard/<int:facultyId>/<int:qid>/<str:facultyName>/', faculty_dashboard, name='facultyView'),
    path('moderator_dashboard/<int:adminId>/<int:qid>/<str:adminName>/', admin_dashboard, name='adminView'),
]
