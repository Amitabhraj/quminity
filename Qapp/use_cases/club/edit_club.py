from django.shortcuts import render

def EditClub(request,CludId):
    return render(request,'/ClubEvent/club/manage-club.html')