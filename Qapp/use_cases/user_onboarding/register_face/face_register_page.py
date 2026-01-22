from django.shortcuts import render

# Create your views here.
def face_register_page(request):
    return render(request, 'html/dashboard/register_face.html')