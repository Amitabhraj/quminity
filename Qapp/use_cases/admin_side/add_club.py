from django.http import JsonResponse
from django.contrib.auth import get_user_model
from Qapp import models

User = get_user_model()


from django.shortcuts import render, redirect
from .models import Club, ClubMembership, ClubGallery

def create_club_view(request):
    if request.method == "POST":
        # 1. Save Basic Info
        club = Club.objects.create(
            club_name=request.POST.get('club_name'),
            description=request.POST.get('description'),
            logo=request.FILES.get('logo'),
            entry_fees=request.POST.get('fee_amount') or 0,
        )

        # 2. Save Gallery Images (Multiple)
        gallery_images = request.FILES.getlist('gallery')
        for img in gallery_images:
            ClubGallery.objects.create(club=club, image=img)

        # 3. Save Organization Structure (President, VP, etc)
        user_ids = request.POST.getlist('user_id[]')
        positions = request.POST.getlist('pos[]')
        
        for uid, pos in zip(user_ids, positions):
            if uid: # Ensure ID is not empty
                ClubMembership.objects.create(
                    club=club, 
                    user_id=uid, 
                    position=pos.upper()
                )

        # 4. Save Core Members
        core_user_ids = request.POST.getlist('core_user_id[]')
        for cuid in core_user_ids:
            if cuid:
                ClubMembership.objects.create(
                    club=club, 
                    user_id=cuid, 
                    position='CORE MEMBER'
                )

        return redirect('club_list') # Redirect to your success page

    return render(request, 'html/moderator/create_club.html')


def search_members_api(request):
    query = request.GET.get('q', '')
    if len(query) >= 6:
        # Search by QID (username) or Full Name
        users = User.objects.filter(
            models.Q(username__icontains=query) | 
            models.Q(first_name__icontains=query)
        )[:10]
        
        results = [
            {'id': user.id, 'text': f"{user.username} - {user.get_full_name()}"} 
            for user in users
        ]
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})