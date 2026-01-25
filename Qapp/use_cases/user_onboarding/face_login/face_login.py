from django.shortcuts import render
import cv2
import numpy as np
import mediapipe as mp
import face_recognition
import pickle
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.contrib.auth.models import User

# --- INITIALIZATION ---
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)

def get_ear(landmarks, w, h):
    def eye_ratio(indices):
        p = [np.array([landmarks[i].x * w, landmarks[i].y * h]) for i in indices]
        return (np.linalg.norm(p[1]-p[5]) + np.linalg.norm(p[2]-p[4])) / (2.0 * np.linalg.norm(p[0]-p[3]))
    return (eye_ratio([362, 385, 387, 263, 373, 380]) + eye_ratio([33, 160, 158, 133, 153, 144])) / 2.0

def detect_spoof(img, gray):
    lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    dft = np.fft.fftshift(np.fft.fft2(gray))
    magnitude_spectrum = 20 * np.log(np.abs(dft) + 1)
    fft_mean = np.mean(magnitude_spectrum)
    # Thresholds (Lower lap_var or higher fft_mean = Spoof)
    if lap_var < 35 or fft_mean > 135:
        return True
    return False

@csrf_exempt
def login_with_face(request):
    if request.method != "POST":
        return JsonResponse({"success": False})

    frame_file = request.FILES.get("frame")
    username = request.POST.get("username") # Pass username from frontend if needed
    
    if not frame_file:
        return JsonResponse({"success": False, "message": "CAMERA ERROR"})

    # Decode Image
    img = cv2.imdecode(np.frombuffer(frame_file.read(), np.uint8), cv2.IMREAD_COLOR)
    h, w, _ = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 1. Anti-Spoofing
    if detect_spoof(img, gray):
        return JsonResponse({"success": False, "message": "SPOOF DETECTED: USE REAL FACE"})

    # 2. Face Detection & 3D Depth
    results = face_mesh.process(rgb_img)
    if not results.multi_face_landmarks:
        return JsonResponse({"success": False, "message": "FACE NOT DETECTED"})

    landmarks = results.multi_face_landmarks[0].landmark
    if abs(landmarks[1].z - landmarks[234].z) < 0.05: # Depth check
        return JsonResponse({"success": False, "message": "ANTI-SPOOF: 3D FACE REQUIRED"})

    # 3. Blink Detection
    ear = get_ear(landmarks, w, h)
    session = request.session
    if 'login_blinks' not in session:
        session['login_blinks'] = 0
        session['login_closed'] = False

    if ear < 0.20:
        session['login_closed'] = True
    elif ear > 0.25 and session.get('login_closed'):
        session['login_blinks'] += 1
        session['login_closed'] = False
    session.modified = True

    # 4. Final Verification (When 2 blinks reached)
    if session['login_blinks'] >= 2:
        # Get user (This example uses request.user, but for Login page you'd find user by username)
        # user = User.objects.get(username=username) 
        user = request.user 
        
        if not user.face_encoding:
            return JsonResponse({"success": False, "message": "NO REGISTERED FACE FOUND"})

        saved_encoding = pickle.loads(user.face_encoding)
        current_encodings = face_recognition.face_encodings(rgb_img)

        if current_encodings:
            match = face_recognition.compare_faces([saved_encoding], current_encodings[0], tolerance=0.5)
            if match[0]:
                login(request, user) # Successfully log the user in
                del session['login_blinks']
                del session['login_closed']
                return JsonResponse({"success": True, "message": "FACE VERIFIED SUCCESSFULLY", "verified": True})
            else:
                return JsonResponse({"success": False, "message": "FACE DOES NOT MATCH"})
        else:
            return JsonResponse({"success": False, "message": "Possible Photo/Video Attack Detected"})

    return JsonResponse({"success": True, "message": "BLINK YOUR EYES TO VERIFY SEVERAL TIMES", "verified": False})

def face_login_page(request):
    return render(request, 'html/dashboard/login_face.html')  
