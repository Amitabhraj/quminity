import pickle
import secrets
import string
import random
import cv2
import numpy as np
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import login as django_login
from Qapp.models import CustomUser

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
    if lap_var < 38 or lap_var > 900: is_real = False
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
        
        file = request.FILES.get("frame")
        name, qid, email = request.POST.get("name"), request.POST.get("qid"), request.POST.get("email")

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

            if CustomUser.objects.filter(qid=qid).exists():
                return JsonResponse({"success": False, "message": "QID already registered"})

            username = f"{name.split(' ')[0]}_{qid}"
            user = CustomUser(
                username=username, email=email, first_name=name,
                qid=qid, user_type="Student", 
                face_encoding=pickle.dumps(feature_to_save) 
            )
            password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
            user.set_password(password)
            user.save()

            EmailMessage("Reg Success", f"User: {username}\nPass: {password}", 
                         settings.DEFAULT_FROM_EMAIL, [email]).send()
            
            django_login(request, user)
            for k in ['reg_otp', 'otp_verified']: session.pop(k, None)
            session.modified = True
            return JsonResponse({"success": True, "message": "SUCCESS"})

        except Exception as e:
            return JsonResponse({"success": False, "message": f"System Error: {str(e)}"})

    return JsonResponse({"success": False, "message": "Invalid Action"})

def face_register_page(request):
    return render(request, 'html/userOnboarding/register/register_face.html')