import random
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from Qapp.models import Club, ClubMembership, ClubGallery

User = get_user_model()

def send_club_otp(request):
    """Generates and sends OTP to the moderator's email via AJAX."""
    if request.method == "POST":
        otp = str(random.randint(100000, 999999))
        request.session['club_creation_otp'] = otp
        
        subject = "Verification Required: Create New Club"
        message = f"Your security OTP for club creation is: {otp}. If you did not initiate this, please ignore this email."
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [request.user.email]
        
        try:
            send_mail(subject, message, email_from, recipient_list)
            return JsonResponse({'status': 'success', 'message': 'OTP sent successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def createClub(request):
    if request.method == "POST":
        # OTP Verification Check
        user_otp = request.POST.get('otp_code')
        session_otp = request.session.get('club_creation_otp')

        if not user_otp or user_otp != session_otp:
            # Handle failed OTP (In production, use django.contrib.messages)
            return redirect('createClub') 

        # Clear OTP session after successful verification
        del request.session['club_creation_otp']

        fee_val = request.POST.get('fee_amount') if request.POST.get('fees') == 'PAID' else 0

        # 1. Save Basic Info
        club = Club.objects.create(
            club_name=request.POST.get('club_name'),
            description=request.POST.get('description'),
            logo=request.FILES.get('logo'),
            entry_fees=fee_val or 0,
        )

        # 2. Save Gallery Images (Multiple)
        gallery_images = request.FILES.getlist('gallery')
        for img in gallery_images:
            ClubGallery.objects.create(club=club, image=img)

        # 3. Save Organization Structure (President, VP, etc)
        user_ids = request.POST.getlist('user_id[]')
        positions = request.POST.getlist('pos[]')
        for uid, pos in zip(user_ids, positions):
            if uid:
                ClubMembership.objects.create(club=club, user_id=uid, position=pos.upper())

        # 4. Save Core Members
        core_user_ids = request.POST.getlist('core_user_id[]')
        for cuid in core_user_ids:
            if cuid:
                ClubMembership.objects.create(club=club, user_id=cuid, position='CORE MEMBER')

        return redirect('/') # Redirect to Dashboard/Home

    return render(request, 'html/ClubEvent/club/create-club.html')