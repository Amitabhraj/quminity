from django.urls import path
from Qapp.qr_code.student.scan_qr import scan_attendance_qr
from Qapp.use_cases.attendance.attendance_forward_dean import ForwardAttendanceNotificationToDean
from Qapp.use_cases.attendance.markAttendance import ApproveEventAttendance
from Qapp.use_cases.club.ClubPayment import CreateClubPayment
from Qapp.use_cases.certificate.emailCertificate import GenerateCertificate
from Qapp.use_cases.dean_side.DeanView import DashboardDean
from Qapp.use_cases.event.manage_event import manageEvent
from Qapp.use_cases.event.EventPayment import CreateEventPayment
from Qapp.use_cases.payment.paymentStatus import PaymentStatus
from Qapp.use_cases.payment.VerifyPayment import VerifyPayment
from Qapp.use_cases.listing.listClubEvent import ClubEventList
from Qapp.use_cases.student_side.studentDiscussion import studentDiscussion
from Qapp.use_cases.student_side.studentAcademics import studentAcad
from .views import *
from .use_cases.listing.listAssociatedClubEvent import ShowAssociatedClub
from .use_cases.user_onboarding.logout_user import user_logout
from .use_cases.user_onboarding.user_login import user_login
from .use_cases.student_side.studentView import MainView as student_dashboard
from .use_cases.faculty_side.facultyView import MainView as faculty_dashboard
from .use_cases.admin_side.adminView import MainView as admin_dashboard
from Qapp.qr_code.instructor import EventQrCode
from Qapp.qr_code.instructor.generateToken import GenerateQR
from Qapp.qr_code.instructor.validateAttend import validate_attendance
from Qapp.use_cases.chatting.chatting import demoChat

urlpatterns = [
    path('', check_authentication, name='check_authentication'),
    path('login/', user_login, name='user_login'),
    path('logout_user/', user_logout, name='user_logout'),


    ############# QR CODE ATTENDANCE #############
    path('show-event-qr/<int:eventId>/', EventQrCode.QrGeneratePage, name='Show_Attendance_QR'),
    path('api/GenerateAttendanceQR/<int:eventId>/', GenerateQR, name='GenerateQR'),

    path('scan-attendance-qr/', scan_attendance_qr, name='scan_page'),
    path('api/validate-attendance/', validate_attendance, name='validate_attendance'),
    ############### QR CODE ATTENDANCE End #############


    #################### Attendance ###############################
    path('ForwardAttendanceToDean/<int:eventId>/', ForwardAttendanceNotificationToDean, name='ForwardAttendanceToDean'),
    path('approve-event-attendance-by-dean/',ApproveEventAttendance,name='ApproveEventAttendance'),
    path('attendace-event-list/<int:eventId>/',ListEventAttendace,name='ListEventAttendace'),
    ##################### Attendance End ##########################


    
    ####################### Payments ########################
    path("payment-club/<int:clubId>/", CreateClubPayment, name="create_payment_club"),
    path("payment-event/<int:eventId>/", CreateEventPayment, name="create_payment_event"),
    path("payment-verification/", VerifyPayment, name="payment_success"),
    path("payment-status/<str:order_id>/", PaymentStatus, name="payment_done"),
    ######################## Payments End ###################

    
    ############### Messaging ####################
    path('demo_chat/', demoChat, name='demoChat'),
    ################## Messaging End #############


    ########################## Manage Club/Events Start ############################
    path('manage-club-events/', ShowAssociatedClub, name='ShowClubEvents'),
    path('manage-club/', ShowAssociatedClub, name='ShowClubEvents'),
    path('manage-event/<int:eventId>/', manageEvent, name='ManageEvent'),
    ########################## Manage Club/Events End ############################

    ###################### Main Pages Start ########################################
    path('studentAcad/<int:studentId>/<int:qid>/<str:studentName>/', studentAcad, name='studentAcad'),
    path('ListClubEvents/', ClubEventList, name='ClubEventList'),
    path('studentDiscussion/<int:studentId>/<int:qid>/<str:studentName>/', studentDiscussion, name='studentDiscussion'),
    ##################### Main Pages Start End ####################################


    ################################ Certificate ##########################
    path('generate-certificate-event/<int:eventId>/', GenerateCertificate, name='GenerateCertificate'),
    ################################ Certificate End ######################

    path('student_dashboard/', student_dashboard, name='studentView'),
    path('dean_dashboard/', DashboardDean, name='DeanDashboard'),
    path('teacher_dashboard/<int:FacultyId>/<int:qid>/<str:facultyName>/', faculty_dashboard, name='facultyView'),
    path('moderator_dashboard/<int:adminId>/<int:qid>/<str:adminName>/', admin_dashboard, name='adminView'),
]
