from django.shortcuts import render


def MainView(request, FacultyId, facultyName):
    context = {
        'studentId': facultyId,
        'studentName': facultyName,
    }
    return render(request, 'html/student_side/student_dashboard.html', context)