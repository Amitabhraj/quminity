from django.shortcuts import render
from Qapp.use_cases.student_side.check_student_cred import check_cred


def studentDiscussion(request, studentId, qid, studentName):
    student_obj = check_cred(request, studentId, qid, studentName) 
    student_section = student_obj.section
    subject_names = list(student_section.subjects.values_list('subjects', flat=True))

    context = {
        'section':student_section,
        'subjects':subject_names
    }

    return render(request,'html/dashboard/studentDiscussion.html',context)