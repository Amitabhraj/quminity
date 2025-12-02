from django.shortcuts import render


def demoChat(request):
    return render(request,'html/dashboard/chatting.html')