from django.shortcuts import render

def MainView(request, studentId, studentName):
    return render(request, 'html/dashboard/index.html')

