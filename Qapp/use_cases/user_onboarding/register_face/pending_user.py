from django.http import HttpResponse
from django.shortcuts import redirect, render
from Qapp.models import CustomUser, PendingUser

def pending_user(request, registration_number):
    # 1. Check if the user is already approved in CustomUser
    if CustomUser.objects.filter(registration_number=registration_number, approved=True).exists():
        return redirect('/')

    # 2. Check if a PendingUser exists for this number
    pending_user_obj = PendingUser.objects.filter(registration_number=registration_number).first()
    
    # 3. Check if a CustomUser exists but is NOT approved
    custom_user_obj = CustomUser.objects.filter(registration_number=registration_number).first()

    if not pending_user_obj and not custom_user_obj:
        return HttpResponse("<b>ERROR: Registration number not found.</b>")

    if pending_user_obj and not pending_user_obj.approved:
        # If user is in PendingUser table, render the pending template
        context = {
            'registration_number': registration_number
        }
        return render(request, 'html/userOnboarding/register/pending_user.html', context)
    
    elif (pending_user_obj.approved and not custom_user_obj) or (pending_user_obj.approved and not custom_user_obj.approved):
        # If CustomUser exists but approved=False
        return HttpResponse(
            "<b>Your user registration request was received and Approved, but Admin has not approved you as a USER.<br>"
            "<center>or</center><br>"
            "ADMIN DISAPPROVED/BLOCKED you as a USER. Please Contact Admin for Approval.</b>"
        )

    # 4. Fallback if no matching registration number is found
    return HttpResponse("<b>ERROR: Registration number not found.</b>")