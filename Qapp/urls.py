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
from Qapp.qr_code import qrCode
from Qapp.qr_code.generateToken import GenerateQR
from Qapp.qr_code.validateAttend import validate_attendance


urlpatterns = [
    path('', check_authentication, name='check_authentication'),
    path('login/', user_login, name='user_login'),


    ############# QR CODE ATTENDANCE #############
    # Instructor
    path('ShowClubForAttendance/', qrCode.ShowAssociatedClub, name='instructor_page'),
    path('Show-Attendance-QR/<int:club_id>/', qrCode.QrGeneratePage, name='Show_Attendance_QR'),
    path('api/GenerateQR/<int:club_id>/', GenerateQR, name='GenerateQR'),

    # Student
    path('scan/', qrCode.scan_page, name='scan_page'),
    path('api/validate/', validate_attendance, name='validate_attendance'),
    #############################################


    path("payment-club/<int:clubId>/<str:clubName>/<int:amount>/", create_payment, name="create_payment"),
    path("payment-success/", payment_success, name="payment_success"),
    path("payment-done/<str:order_id>/", payment_done, name="payment_done"),


    path('logout_user/', user_logout, name='user_logout'),

    path('studentAcad/<int:studentId>/<int:qid>/<str:studentName>/', studentAcad, name='studentAcad'),
    path('studentClub/<int:studentId>/<int:qid>/<str:studentName>/', studentClub, name='studentClub'),
    path('studentDiscussion/<int:studentId>/<int:qid>/<str:studentName>/', studentDiscussion, name='studentDiscussion'),


    path('student_dashboard/<int:studentId>/<int:qid>/<str:studentName>/', student_dashboard, name='studentView'),
    path('teacher_dashboard/<int:FacultyId>/<int:qid>/<str:facultyName>/', faculty_dashboard, name='facultyView'),
    path('moderator_dashboard/<int:adminId>/<int:qid>/<str:adminName>/', admin_dashboard, name='adminView'),
]
