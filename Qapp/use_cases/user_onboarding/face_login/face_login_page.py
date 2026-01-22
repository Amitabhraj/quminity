from django.shortcuts import render

# Create your views here.
def face_login_page(request):
    return render(request, 'html/dashboard/login_face.html')  