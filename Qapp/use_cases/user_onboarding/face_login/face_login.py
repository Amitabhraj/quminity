import pickle
import cv2
from django.http import JsonResponse
from django.shortcuts import render
import face_recognition
from django.contrib.auth import login as django_login
from django.views.decorators.csrf import csrf_exempt
from Qapp.models import CustomUser
import numpy as np
import mediapipe as mp


mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)


def get_ear(landmarks, w, h):
    def eye_ratio(indices):
        p = [np.array([landmarks[i].x * w, landmarks[i].y * h]) for i in indices]
        return (np.linalg.norm(p[1]-p[5]) + np.linalg.norm(p[2]-p[4])) / (2.0 * np.linalg.norm(p[0]-p[3]))
    return (eye_ratio([362, 385, 387, 263, 373, 380]) + eye_ratio([33, 160, 158, 133, 153, 144])) / 2.0


@csrf_exempt
def login_with_face(request):
    if request.method != "POST":
        return render(request, 'html/dashboard/login_face.html')

    action = request.POST.get("action")
    session = request.session

    if action == "clear_session":
        for key in ['blinks', 'closed']:
            session.pop(key, None)
        session.modified = True
        return JsonResponse({"success": True})

    if action == "login_face":
        file = request.FILES.get("frame")
        qid = int(request.POST.get("qid"))
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
        if lap_var < 13 or fft_score < 115 or depth_diff < 0.06:
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
            current_enc = face_recognition.face_encodings(rgb_img, [box])

            if current_enc:
                # Get all users who have a face encoding
                users = CustomUser.objects.filter(qid=qid).exclude(face_encoding__isnull=True)
                
                # Extract all encodings and user IDs
                known_encodings = []
                user_map = []
                
                for user in users:
                    try:
                        known_encodings.append(pickle.loads(user.face_encoding))
                        user_map.append(user)
                    except:
                        continue
                
                if not known_encodings:
                    return JsonResponse({"success": False, "message": "FACE DOES NOT MATCHED"})

                # Compare live face against the entire database
                # Tolerance 0.45 is stricter for 1:N matching to avoid false positives
                matches = face_recognition.compare_faces(known_encodings, current_enc[0], tolerance=0.45)
                
                if True in matches:
                    first_match_index = matches.index(True)
                    matched_user = user_map[first_match_index]
                    
                    # Login the matched user
                    django_login(request, matched_user)
                    
                    # Clean session
                    [session.pop(k, None) for k in ['blinks', 'closed']]
                    return JsonResponse({
                        "success": True, 
                        "authenticated": True, 
                        "message": f"Welcome, {matched_user.first_name}!"
                    })
                else:
                    return JsonResponse({"success": False,"face_detected": False, "message": "FACE DOES NOT MATCHED"})

        return JsonResponse({"success": True, "face_detected": True, "message": "BLINK TO IDENTIFY"})




def face_login_page(request):
    return render(request, 'html/userOnboarding/login/login_face.html')

