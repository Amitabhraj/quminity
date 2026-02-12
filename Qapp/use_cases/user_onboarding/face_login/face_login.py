import cv2
import numpy as np
import os
import base64
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as django_login
from Qapp.models import CustomUser, PendingUser
from quminity.settings import BASE_DIR

# --- INITIALIZATION ---
YUNET_PATH = os.path.join(BASE_DIR, 'face_detection_yunet_2023mar.onnx')
SFACE_PATH = os.path.join(BASE_DIR, 'face_recognition_sface_2021dec.onnx')

detector = cv2.FaceDetectorYN.create(
    model=YUNET_PATH, config="", input_size=(320, 320),
    score_threshold=0.9, nms_threshold=0.3, top_k=5000,
    backend_id=3, target_id=0
)

recognizer = cv2.FaceRecognizerSF.create(
    model=SFACE_PATH, config="", backend_id=3, target_id=0
)

def perform_liveness_check(img, face_data):
    x, y, w, h = face_data[0:4].astype(int)
    face_roi = img[max(0, y):y+h, max(0, x):x+w]
    if face_roi.size == 0: return False

    gray_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
    lap_var = cv2.Laplacian(gray_roi, cv2.CV_64F).var()

    landmarks = face_data[4:14].reshape((5, 2))
    eye_dist = np.linalg.norm(landmarks[0] - landmarks[1])
    ratio = eye_dist / w

    if lap_var < 22 or lap_var > 900: return False
    if ratio < 0.22 or ratio > 0.5: return False
    return True

@csrf_exempt
def login_with_face(request):
    if request.method != "POST":
        return render(request, 'html/userOnboarding/login/login_face.html')

    action = request.POST.get("action")
    if action == "login_face":
        file = request.FILES.get("frame")
        qid_val = request.POST.get("qid")
        
        if not file or not qid_val:
            return JsonResponse({"success": False, "message": "Missing frame or QID"})
        
        try:
            # 1. Image Decoding
            img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
            h, w, _ = img.shape

            # 2. Face Detection
            detector.setInputSize((w, h))
            _, faces = detector.detect(img)

            if faces is None or len(faces) == 0:
                return JsonResponse({"success": False, "message": "Face not detected"})

            face_data = faces[0]

            # 3. Liveness Check
            if not perform_liveness_check(img, face_data):
                return JsonResponse({"success": False, "message": "Spoof Detected: Real face required!"})

            # 4. Feature Extraction (Current Live Face)
            aligned_face = recognizer.alignCrop(img, face_data)
            current_feature = recognizer.feature(aligned_face)
            current_feature = np.array(current_feature, dtype=np.float32).reshape(1, -1)

            # 5. Database Retrieval
            user = CustomUser.objects.filter(qid=qid_val).exclude(face_encoding__isnull=True).first()
            if not user:
                user = PendingUser.objects.filter(qid=qid_val).exclude(face_encoding__isnull=True).first()

            if not user or not user.face_encoding:
                return JsonResponse({"success": False, "message": "User not registered or no face data"})

            # 6. Decode TextField (Base64) to NumPy
            try:
                # Convert the stored string back into bytes
                decoded_bytes = base64.b64decode(user.face_encoding)
                # Reconstruct the 128-float array
                known_feature = np.frombuffer(decoded_bytes, dtype=np.float32).reshape(1, -1)
                
                # Match using SFace (0 = Cosine Similarity)
                score = recognizer.match(current_feature, known_feature, 0)
            except Exception as e:
                return JsonResponse({"success": False, "message": "Biometric format error. Please re-register."})

            # 7. Authentication Logic
            # SFace Cosine threshold is usually around 0.36; 0.5 is very strict/secure.
            if score > 0.45: 
                if hasattr(user, 'user_type') and user.user_type == "STUDENT":
                    django_login(request, user)
                
                return JsonResponse({
                    "success": True, 
                    "authenticated": True,
                    "redirect_url": f"/pending_user/{user.registration_number}",
                    "message": f"Welcome, {getattr(user, 'username', getattr(user, 'name', 'User'))}!"
                })
            else:
                return JsonResponse({"success": False, "message": "Face does not match"})

        except Exception as e:
            return JsonResponse({"success": False, "message": f"Login Error: {str(e)}"})

    return JsonResponse({"success": False, "message": "Invalid Request"})

def face_login_page(request):
    return render(request, 'html/userOnboarding/login/login_face.html')