from django.shortcuts import render
from Qapp.use_cases.student_side.check_student_cred import check_cred


def studentAcad(request, studentId, qid, studentName):
    student_obj = check_cred(request, studentId, qid, studentName) 
    student_section = student_obj.section
    subject = student_section.subject.all()

    context = {
        'section':student_section,
        'subjects':subject
    }

    return render(request,'html/dashboard/studentAcad.html',context)