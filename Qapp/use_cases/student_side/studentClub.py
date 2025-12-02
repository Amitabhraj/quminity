from django.shortcuts import render
from Qapp.models import Club
from Qapp.use_cases.student_side.check_student_cred import check_cred


def studentClub(request, studentId, qid, studentName):
    student_obj = check_cred(request, studentId, qid, studentName) 
    all_club = Club.objects.all()

    context = {
        'club':all_club
    }

    return render(request,'html/dashboard/studentClub.html',context)