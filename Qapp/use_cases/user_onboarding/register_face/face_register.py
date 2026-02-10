from django.utils import timezone
import pickle
import secrets
import string
import random
import cv2
import numpy as np
import os
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import login as django_login
from Qapp.models import CustomUser, PendingUser
from Qapp.use_cases.user_onboarding.common import *

# --- YUNET & SFACE INITIALIZATION (EC2 SAFE) ---
YUNET_PATH = os.path.join(settings.BASE_DIR,'face_detection_yunet_2023mar.onnx')
SFACE_PATH = os.path.join(settings.BASE_DIR, 'face_recognition_sface_2021dec.onnx')

# backend_id=3 (OpenCV) and target_id=0 (CPU) ensures it runs on EC2 Free Tier
detector = cv2.FaceDetectorYN.create(
    model=YUNET_PATH, config="", input_size=(320, 320),
    score_threshold=0.9, nms_threshold=0.3, top_k=5000,
    backend_id=3, target_id=0
)

recognizer = cv2.FaceRecognizerSF.create(
    model=SFACE_PATH, config="",
    backend_id=3, target_id=0
)

# --- UTILITY: PASSIVE LIVENESS CHECK ---
def perform_liveness_check(img, face_data):
    """
    Checks for spoofing using Laplacian Variance (Texture) 
    and Geometric Ratios (3D-to-2D projection consistency).
    """
    x, y, w, h = face_data[0:4].astype(int)
    face_roi = img[max(0, y):y+h, max(0, x):x+w]
    if face_roi.size == 0: 
        return False

    # 1. Texture Check (Laplacian Variance)
    gray_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
    lap_var = cv2.Laplacian(gray_roi, cv2.CV_64F).var()

    # 2. Geometric Ratio Check (Landmark Analysis)
    landmarks = face_data[4:14].reshape((5, 2))
    eye_dist = np.linalg.norm(landmarks[0] - landmarks[1])
    ratio = eye_dist / w 

    print(f"Reg Liveness -> Lap: {lap_var:.2f} | Ratio: {ratio:.4f}")

    # Thresholds tuned for EC2 performance
    is_real = True
    if lap_var < 15 or lap_var > 900: is_real = False
    if ratio < 0.22 or ratio > 0.5: is_real = False 

    return is_real


@csrf_exempt
def register_face(request):
    if request.method != "POST":
        return render(request, 'html/userOnboarding/register/register_face.html')

    action = request.POST.get("action")
    session = request.session

    # --- OTP LOGIC ---
    if action == "send_otp":
        email = request.POST.get("email")
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "message": "Email Already Registered"})
        
        otp = str(random.randint(100000, 999999))
        session['reg_otp'] = otp
        session.modified = True
        try:
            EmailMessage("Your OTP", f"Code: {otp}", settings.DEFAULT_FROM_EMAIL, [email]).send()
            return JsonResponse({"success": True})
        except:
            return JsonResponse({"success": False, "message": "Email Failed"})

    if action == "verify_otp":
        if request.POST.get("otp") == session.get('reg_otp'):
            session['otp_verified'] = True
            session.modified = True
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "message": "Invalid OTP"})

    # --- FACE REGISTRATION LOGIC ---
    if action == "register_face":
        if not session.get('otp_verified'):
            return JsonResponse({"success": False, "message": "Verify Email First"})
        
        print(request.POST)
        
        file = request.FILES.get("frame")
        name = request.POST.get("name")
        qid = request.POST.get("qid")

        user_type = request.POST.get('user_type')

        if not file or not qid:
            return JsonResponse({"success": False, "message": "Missing Data"})

        # Decode & Detect
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        h, w, _ = img.shape
        detector.setInputSize((w, h))
        _, faces = detector.detect(img)

        if faces is None or len(faces) == 0:
            return JsonResponse({"success": False, "message": "No Face Detected"})

        # Liveness Check
        if not perform_liveness_check(img, faces[0]):
            return JsonResponse({"success": False, "message": "Spoof Attack Detected!"})

        # Feature Extraction using SFace
        try:
            aligned_face = recognizer.alignCrop(img, faces[0])
            feature = recognizer.feature(aligned_face) 
            
            # --- CRITICAL FIX: Save as Float32 and Reshape to (1, 128) ---
            # This ensures compatibility with the login matching logic
            feature_to_save = np.array(feature, dtype=np.float32).reshape(1, -1)

            if CustomUser.objects.filter(qid=qid,user_type=user_type).exists():
                return JsonResponse({"success": False, "message": "QID already registered !! Contact Admin for Solution"})

            username = f"{name.split(' ')[0]}_{qid}"

            USER_TYPE_VARIABLE = [item[0] for item in USER_TYPE]
            registration_number = random.choice(string.ascii_uppercase) + ''.join(str(random.randint(0, 9)) for _ in range(6))
            
            if user_type in USER_TYPE_VARIABLE and user_type != "STUDENT":
                email = request.POST.get("email")
                mobile_number = request.POST.get('phone')

                pendinguser = PendingUser(
                    username=username,
                    email=email,
                    qid=qid,
                    user_type=user_type, 
                    face_encoding=pickle.dumps(feature_to_save),
                    mobile = mobile_number,
                    user_requested_at = timezone.now(),
                    registration_number=registration_number
                )
                pendinguser.save()
                EmailMessage(
                    "Regards User Registration",
                    f"We Have Successfully Sent your request for User Registeration to the ADMIN\n\nUser: {pendinguser.username}\nMobile Number: {pendinguser.mobile}", 
                    settings.DEFAULT_FROM_EMAIL, 
                    [email]).send()
                
                return JsonResponse({"success": True, 
                                     "registered":True,
                                    "redirect_url": f"/pending_user/{registration_number}/", 
                                    "message": "Registration Request Sent Successfully"
                                })
                
            elif user_type == "STUDENT":
                email = request.POST.get("email")
                mobile_number = request.POST.get('phone')
                program = request.POST.get('program')
                branch = request.POST.get('branch')
                section = request.POST.get('section')
                year = request.POST.get('year')

                user = CustomUser(
                    username=username,
                    email=email,
                    first_name=name,
                    qid=qid,
                    user_type=user_type, 
                    face_encoding=pickle.dumps(feature_to_save),
                    mobile = mobile_number,
                    program = program,
                    current_year=year,
                    approved=True,
                    branch=branch,
                    section=section,
                    registration_number=registration_number,
                    registered_at = timezone.now(),
                    updated_at = timezone.now()
                )
                password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
                user.set_password(password)
                user.save()

                for k in ['reg_otp', 'otp_verified']: session.pop(k, None)
                session.modified = True

                EmailMessage("Registration Successfull", f"User: {username}\nPassword: {password}", 
                            settings.DEFAULT_FROM_EMAIL, [email]).send()
            
                django_login(request, user)
                for k in ['reg_otp', 'otp_verified']: session.pop(k, None)
                session.modified = True
                return JsonResponse({"success": True,
                                     "registered":True,
                                     "redirect_url": f"/pending_user/{registration_number}/",
                                     "message": "SUCCESS"})

        except Exception as e:
            return JsonResponse({"success": False, "message": f"System Error: {str(e)}"})

    return JsonResponse({"success": False, "message": "Invalid Action"})

def face_register_page(request):
    context = {
        'USER_TYPE':USER_TYPE,
        'courses_name_choices':courses_name_choices,
        "branch_choices":branch_choices,
        'section_choices':section_choices,
        'current_year_choices':current_year_choices
    }
    return render(request, 'html/userOnboarding/register/register_face.html',context)


