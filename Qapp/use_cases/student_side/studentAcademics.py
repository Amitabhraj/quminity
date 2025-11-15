from django.shortcuts import render
from Qapp.use_cases.student_side.check_student_cred import check_cred


def studentAcad(request, studentId, qid, studentName):
    student_obj = check_cred(request, studentId, qid, studentName) 
    student_section = student_obj.section
    subject_names = list(student_section.subject.values_list('subject_name', flat=True))

    context = {
        'section':student_section,
        'subjects':subject_names
    }

    return render(request,'html/dashboard/studentAcad.html',context)