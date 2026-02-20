from django.shortcuts import render

def EditClub(request,CludId):
    return render(request,'/html/ClubEvent/club/manage-club.html')