from django.shortcuts import render


def demoChat(request):
    return render(request,'dashboard/chatting.html')