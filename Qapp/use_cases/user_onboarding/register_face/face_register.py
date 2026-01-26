from datetime import datetime
from django.contrib.auth.models import Group
import secrets
import string
import cv2
import numpy as np
import mediapipe as mp
import face_recognition
from django.contrib.auth import authenticate, login
import pickle
import random
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.conf import settings
from Qapp.models import CustomUser

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)

def get_ear(landmarks, w, h):
    def eye_ratio(indices):
        p = [np.array([landmarks[i].x * w, landmarks[i].y * h]) for i in indices]
        return (np.linalg.norm(p[1]-p[5]) + np.linalg.norm(p[2]-p[4])) / (2.0 * np.linalg.norm(p[0]-p[3]))
    return (eye_ratio([362, 385, 387, 263, 373, 380]) + eye_ratio([33, 160, 158, 133, 153, 144])) / 2.0

def get_fft_score(gray_img):
    dft = np.fft.fft2(gray_img)
    dft_shift = np.fft.fftshift(dft)
    mag = 20 * np.log(np.abs(dft_shift) + 1)
    return np.mean(mag)

@csrf_exempt
def register_face(request):
    if request.method != "POST":
        return render(request, 'html/dashboard/register_face.html')

    action = request.POST.get("action")
    session = request.session

    if action == "clear_session":
        for key in ['blinks', 'closed', 'is_saving']:
            session.pop(key, None)
        return JsonResponse({"success": True})

    if action == "send_otp":
        email = request.POST.get("email")
        try:
            existing_user = CustomUser.objects.get(email=email)
            [session.pop(k, None) for k in ['blinks', 'closed', 'reg_otp', 'otp_verified', 'is_saving']]
            return JsonResponse({"success": False, "message": "Email Already Registered"})
        except CustomUser.DoesNotExist:
            pass
        otp = str(random.randint(100000, 999999))
        session['reg_otp'] = otp
        try:
            EmailMessage("Your OTP", f"Code: {otp}", settings.DEFAULT_FROM_EMAIL, [email]).send()
            return JsonResponse({"success": True})
        except:
            return JsonResponse({"success": False, "message": "Email Failed"})

    if action == "verify_otp":
        if request.POST.get("otp") == session.get('reg_otp'):
            session['otp_verified'] = True
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "message": "Invalid OTP"})

    if action == "register_face":
        if not session.get('otp_verified'):
            return JsonResponse({"success": False, "message": "Verify Email First"})
        
        name = request.POST.get("name")
        qid = request.POST.get("qid")
        email = request.POST.get("email")

        try:
            existing_user = CustomUser.objects.get(qid=qid)
            [session.pop(k, None) for k in ['blinks', 'closed', 'reg_otp', 'otp_verified', 'is_saving']]
            return JsonResponse({"qid_found": True, "message": "QID Already Registered"})
        except CustomUser.DoesNotExist:
            pass

        file = request.FILES.get("frame")
        
        # Decode Image
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        h, w, _ = img.shape
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 1. Face Mesh Analysis
        results = face_mesh.process(rgb_img)
        if not results.multi_face_landmarks and not session.get('is_saving'):
            return JsonResponse({"success": False, "message": "Face not in Frame"})

        landmarks = results.multi_face_landmarks[0].landmark

        # 2. Enhanced Spoof Check
        # Laplacian: Sharpness check
        lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # FFT: Screen Pattern Check
        dft = np.fft.fftshift(np.fft.fft2(gray))
        mag = 20 * np.log(np.abs(dft) + 1)
        cy, cx = h // 2, w // 2
        y, x = np.ogrid[:h, :w]
        mask = ((x - cx)**2 + (y - cy)**2 >= 40**2) & ~((x - cx)**2 + (y - cy)**2 <= 20**2)
        fft_score = np.mean(mag[mask]) if np.any(mask) else 0

        # 3D Depth check (The 'Z' distance from eyes to nose tip)
        nose_z = landmarks[1].z
        eyes_z = (landmarks[33].z + landmarks[263].z) / 2
        depth_diff = abs(nose_z - eyes_z)

        print("lap_var:", lap_var, "fft_score:", fft_score, " depth_diff:", depth_diff)

        # Validation Logic
        if lap_var < 37 or fft_score < 122 or depth_diff < 0.06:
            if not session.get('is_saving'):
                return JsonResponse({"success": False, "message": "Face is Not Clear"})

        ear = get_ear(landmarks, w, h)
        if 'blinks' not in session:
            session['blinks'], session['closed'] = 0, False

        if ear < 0.20:
            session['closed'] = True
        elif ear > 0.25 and session.get('closed'):
            session['blinks'] += 1
            session['closed'] = False
        session.modified = True

        if session['blinks'] >= 2:
            all_x = [l.x * w for l in landmarks]
            all_y = [l.y * h for l in landmarks]
            box = (int(min(all_y)), int(max(all_x)), int(max(all_y)), int(min(all_x)))
            enc = face_recognition.face_encodings(rgb_img, [box])
            if enc:
                if not session.get('is_saving'):
                    session['is_saving'] = True
                    session.modified = True
                    return JsonResponse({
                        "success": True, 
                        "processing": True, 
                        "message": "WAIT... WE ARE PROCESSING YOUR REQUEST..."
                    })

                try:
                    user = CustomUser(
                        username=f"{name.split(' ')[0]}_{qid}",
                        email=email, 
                        first_name=name,
                        qid=qid,
                        user_type="Student",
                        face_encoding=pickle.dumps(enc[0])
                    )
                    user.save()
                    
                    alphabet = string.ascii_letters + string.digits + string.punctuation
                    password = ''.join(secrets.choice(alphabet) for _ in range(12))
                    user.set_password(password)
                    user.save()

                    # Emailing
                    EmailMessage(
                        "Registration Successful",
                        f"Username: {user.username}\nPassword: {password}\nQID: {qid}\n...",
                        settings.DEFAULT_FROM_EMAIL,
                        [email]
                    ).send()

                    authenticate_user = authenticate(username=user.username, password=password)
                    if authenticate_user:
                        login(request, authenticate_user)
                        [session.pop(k, None) for k in ['blinks', 'closed', 'reg_otp', 'otp_verified', 'is_saving']]
                        return JsonResponse({"success": True, "registered": True, "message": "REGISTRATION SUCCESSFUL"})
                except Exception as e:
                    session['is_saving'] = False # Reset on error
                    return JsonResponse({"success": False, "message": f"Error: {str(e)}"})

        return JsonResponse({"success": True, "face_detected": True, "message": "PLEASE BLINK YOUR EYES"})

    return JsonResponse({"success": False, "message": "Invalid Action"})


def face_register_page(request):
    return render(request, 'html/userOnboarding/register/register_face.html') 