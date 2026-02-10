import pickle
import cv2
import numpy as np
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as django_login
from Qapp.models import CustomUser, PendingUser
from quminity.settings import BASE_DIR # Best practice to use settings.BASE_DIR

# --- YUNET & SFACE INITIALIZATION ---
YUNET_PATH = os.path.join(BASE_DIR, 'face_detection_yunet_2023mar.onnx')
SFACE_PATH = os.path.join(BASE_DIR, 'face_recognition_sface_2021dec.onnx')

detector = cv2.FaceDetectorYN.create(
    model=YUNET_PATH, config="", input_size=(320, 320),
    score_threshold=0.9, nms_threshold=0.3, top_k=5000
)
# Explicitly tell OpenCV to use CPU to prevent terminal hanging on EC2
detector = cv2.FaceDetectorYN.create(
    model=YUNET_PATH, 
    config="", 
    input_size=(320, 320),
    score_threshold=0.9, 
    nms_threshold=0.3, 
    top_k=5000,
    backend_id=3,
    target_id=0
)

recognizer = cv2.FaceRecognizerSF.create(
    model=SFACE_PATH, 
    config="",
    backend_id=3,
    target_id=0
)
# --- UTILITY: PASSIVE LIVENESS CHECK ---
def perform_liveness_check(img, face_data):
    x, y, w, h = face_data[0:4].astype(int)
    face_roi = img[max(0, y):y+h, max(0, x):x+w]
    if face_roi.size == 0: return False

    # Texture
    gray_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
    lap_var = cv2.Laplacian(gray_roi, cv2.CV_64F).var()

    # Landmarks for Geometry (Indices 4-13)
    landmarks = face_data[4:14].reshape((5, 2))
    eye_dist = np.linalg.norm(landmarks[0] - landmarks[1])
    ratio = eye_dist / w

    print(f"Reg Liveness -> Lap: {lap_var:.2f} | Ratio: {ratio:.4f}")

    # Standardized thresholds
    is_real = True
    if lap_var < 22 or lap_var > 900: is_real = False
    if ratio < 0.22 or ratio > 0.5: is_real = False
    
    return is_real

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

            # 2. Face Detection (YuNet)
            detector.setInputSize((w, h))
            _, faces = detector.detect(img)

            if faces is None or len(faces) == 0:
                return JsonResponse({"success": False, "message": "Face not detected"})

            face_data = faces[0]

            # 3. Apply Localized Liveness Check
            if not perform_liveness_check(img, face_data):
                return JsonResponse({"success": False, "message": "Spoof Detected: Real face required!"})

            # 4. Feature Extraction (SFace)
            aligned_face = recognizer.alignCrop(img, face_data)
            current_feature = recognizer.feature(aligned_face)

            # 5. Database Verification
            user = CustomUser.objects.filter(qid=qid_val).exclude(face_encoding__isnull=True).first()
            pendinguser = PendingUser.objects.filter(qid=qid_val).exclude(face_encoding__isnull=True).first()

            if not pendinguser and not user:
                return JsonResponse({"success": False, "message": "User not registered"})
            
            if pendinguser:
                if pendinguser.approved:
                    user = user
                    if not user:
                        return JsonResponse({
                                        "success": True, 
                                        "authenticated": True,
                                        "redirect_url":f"/pending_user/{pendinguser.registration_number}",
                                        "message": f" {pendinguser.name} , You have been Disapproved or Blocked!"
                                    })
                    elif not user.approved:
                        return JsonResponse({
                                        "success": True, 
                                        "authenticated": True,
                                        "redirect_url":f"/pending_user/{user.registration_number}",
                                        "message": f" {user.username} , You have been Disapproved or Blocked!"
                                    })
                else:
                    user = pendinguser
            else:
                user=user

            if user.face_encoding is None:
                return JsonResponse({"success": False, "message": "No face data found. Please contact Admin of this website"})  

            try:
                # 1. Load raw data from pickle
                raw_saved_data = pickle.loads(user.face_encoding)
                
                # 2. Convert BOTH to float32 and FLATTEN them to (1, 128)
                # SFace MUST have (1, 128) shape for the match function
                known_feature = np.array(raw_saved_data, dtype=np.float32).reshape(1, -1)
                current_feature = np.array(current_feature, dtype=np.float32).reshape(1, -1)

                # 3. Calculate Cosine Similarity (0 = FR_COSINE)
                score = recognizer.match(current_feature, known_feature, 0)
                
                print(f"Match Score: {score:.4f}")

            except Exception as e:
                # This will catch if the old DB vector is e.g. 512 while SFace is 128
                return JsonResponse({"success": False, "message": f"Incompatible Face Data: Please re-register. Error: {str(e)}"})

            print(f"Login Attempt - QID: {qid_val} | Match Score: {score:.4f}")

            # SFace Cosine Threshold is typically 0.36
            if score > 0.5:
                if user.user_type == "STUDENT":
                    django_login(request, user)
                return JsonResponse({
                    "success": True, 
                    "authenticated": True,
                    "redirect_url":f"/pending_user/{user.registration_number}",
                    "message": f"Welcome, {user.username}!"
                })
            else:
                return JsonResponse({"success": False, "message": "Face does not match"})

        except Exception as e:
            return JsonResponse({"success": False, "message": f"Login Error: {str(e)}"})

    return JsonResponse({"success": False, "message": "Invalid Request"})

def face_login_page(request):      
    return render(request, 'html/userOnboarding/login/login_face.html')