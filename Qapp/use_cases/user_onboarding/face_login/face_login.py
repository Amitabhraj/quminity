import pickle
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import face_recognition
import numpy as np
from Qapp.models import CustomUser
from quminity.settings import BASE_DIR
from django.shortcuts import render

def face_login_page(request):
    return render(request, 'html/dashboard/login_face.html')  


face_cascade = cv2.CascadeClassifier(
    str(BASE_DIR / "haarcascade_frontalface_default.xml")
)

eye_cascade = cv2.CascadeClassifier(
    str(BASE_DIR / "haarcascade_eye_tree_eyeglasses.xml")
)

@csrf_exempt
def login_with_face(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

    # Verify user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "User not authenticated"}, status=401)

    frames = request.FILES.getlist("frames")
    if len(frames) < 5:
        return JsonResponse({"success": False, "message": "Insufficient frames"})

    eye_states = []
    face_positions = []
    texture_scores = []
    face_rois = []
    
    for frame in frames:
        # Your uploaded file is an InMemoryUploadedFile
        # Process it similar to your code
        img_array = np.frombuffer(frame.read(), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        if img is None:
            continue
            
        # Resize if too large for better performance
        height, width = img.shape[:2]
        if width > 800:
            scale = 800 / width
            img = cv2.resize(img, (800, int(height * scale)))
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # You can now use the face_cascade directly
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5, minSize=(150, 150)
        )

        if len(faces) == 0:
            continue

        x, y, w, h = faces[0]
        face_positions.append((x, y, w, h))

        # Extract face ROI from original color image
        face_roi = img[y:y+h, x:x+w]
        face_rois.append(face_roi)
        
        # Extract face ROI from grayscale for eye detection and texture analysis
        roi_gray = gray[y:y+h, x:x+w]

        # Eye detection
        eyes = eye_cascade.detectMultiScale(
            roi_gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30)
        )
        eye_states.append(len(eyes) >= 2)

        # Texture analysis (variance of Laplacian)
        texture = cv2.Laplacian(roi_gray, cv2.CV_64F).var()
        texture_scores.append(texture)
        
        # Reset file pointer for potential reuse
        frame.seek(0)

    # 1️⃣ Face must appear
    if len(face_positions) < 3:
        return JsonResponse({
            "success": False,
            "message": "Face not consistently detected"
        })

    # 2️⃣ Motion check (anti-photo)
    motion_detected = False
    for i in range(1, len(face_positions)):
        x1, y1, _, _ = face_positions[i - 1]
        x2, y2, _, _ = face_positions[i]
        if abs(x1 - x2) > 5 or abs(y1 - y2) > 5:
            motion_detected = True
            break

    if not motion_detected:
        return JsonResponse({
            "success": False,
            "message": "No natural face movement detected (possible photo attack)"
        })

    # 3️⃣ Texture check (flat image detection)
    avg_texture = np.mean(texture_scores)
    if avg_texture < 30:
        return JsonResponse({
            "success": False,
            "message": "Low facial texture detected (possible photo/video attack)"
        })

    # 4️⃣ Blink detection (Open → Closed → Open)
    blink_detected = False
    for i in range(1, len(eye_states) - 1):
        if eye_states[i - 1] and not eye_states[i] and eye_states[i + 1]:
            blink_detected = True
            break

    if not blink_detected:
        return JsonResponse({
            "success": False,
            "message": "Blink not detected"
        })
    

    # 5️⃣ FACE RECOGNITION
    best_face = face_rois[len(face_rois) // 2]
    rgb_face = cv2.cvtColor(best_face, cv2.COLOR_BGR2RGB)

    encodings = face_recognition.face_encodings(rgb_face)
    if not encodings:
        return JsonResponse({"success": False, "message": "Face encoding failed"})
    
    incoming_encoding = encodings[0]
    user = CustomUser.objects.get(id=request.user.id)
    if not user.face_encoding:
        return JsonResponse({"success": False, "message": "Face not registered"})

    stored_encoding = pickle.loads(user.face_encoding)
    matches = face_recognition.compare_faces(
        [stored_encoding],
        incoming_encoding,
        tolerance=0.45
    )

    if not matches[0]:
        return JsonResponse({
            "success": False,
            "message": "Face does not match registered user"
        })

    return JsonResponse({
        "success": True,
        "message": "Face verified successfully. Login approved."
    })