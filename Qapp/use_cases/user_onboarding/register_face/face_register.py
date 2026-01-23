from django.shortcuts import render
import cv2
import numpy as np
import face_recognition
import pickle
import mediapipe as mp
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# --- INITIALIZATION ---
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5
)

# Configuration Thresholds
EAR_THRESHOLD = 0.22
SPOOF_THRESH_LAPLACIAN = 28.0
SPOOF_THRESH_FFT = 45.0
SPOOF_THRESH_SATURATION = 85.0


def face_register_page(request):
    return render(request, 'html/dashboard/register_face.html') 


# Global Initialize
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

@csrf_exempt
def register_face(request):
    if request.method != "POST": return JsonResponse({"success": False}, status=400)
    
    frame_file = request.FILES.get("frame")
    if not frame_file: return JsonResponse({"success": False, "message": "No frame"})

    # Decode Image
    img = cv2.imdecode(np.frombuffer(frame_file.read(), np.uint8), cv2.IMREAD_COLOR)
    h, w, _ = img.shape
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 1. Face Mesh Analysis
    results = face_mesh.process(rgb_img)
    if not results.multi_face_landmarks:
        return JsonResponse({"success": False, "message": "Face not in frame"})

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

    print("fft_score:", fft_score, " lap_var:", lap_var, " depth_diff:", depth_diff)

    # Validation Logic
    if lap_var < 37 or fft_score < 122 or depth_diff < 0.09:
        return JsonResponse({"success": False, "message": "Possible spoof detected"})

    # 3. Blink Logic
    def get_ear(indices):
        p = [np.array([landmarks[i].x * w, landmarks[i].y * h]) for i in indices]
        return (np.linalg.norm(p[1]-p[5]) + np.linalg.norm(p[2]-p[4])) / (2.0 * np.linalg.norm(p[0]-p[3]))

    ear = (get_ear([362, 385, 387, 263, 373, 380]) + get_ear([33, 160, 158, 133, 153, 144])) / 2.0
    
    session = request.session
    if 'blink_count' not in session: session['blink_count'] = 0; session['closed'] = False

    print(ear, session['blink_count'])
    
    if ear < 0.20:
        session['closed'] = True
    elif session.get('closed'):
        session['blink_count'] += 1
        session['closed'] = False
    session.modified = True

    # 4. Success State
    if session['blink_count'] >= 2:
        all_x = [l.x * w for l in landmarks]; all_y = [l.y * h for l in landmarks]
        box = (int(min(all_y)), int(max(all_x)), int(max(all_y)), int(min(all_x)))
        enc = face_recognition.face_encodings(rgb_img, [box])
        if enc:
            user = request.user
            user.face_encoding = pickle.dumps(enc[0])
            user.save()
            del session['blink_count']; del session['closed']
            return JsonResponse({"success": True})

    return JsonResponse({"success": False, "blink_count": session['blink_count'], "message": "Blink your eyes"})