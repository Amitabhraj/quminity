from django.shortcuts import render

def ManageClub(request):
    return render(request,'/html/ClubEvent/club/manage-club.html')