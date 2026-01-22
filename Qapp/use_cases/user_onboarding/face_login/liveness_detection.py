from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import numpy as np
from quminity.settings import BASE_DIR


face_cascade = cv2.CascadeClassifier(
    str(BASE_DIR / "haarcascade_frontalface_default.xml")
)

eye_cascade = cv2.CascadeClassifier(
    str(BASE_DIR / "haarcascade_eye_tree_eyeglasses.xml")
)

@csrf_exempt
def liveness_check(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

    frames = request.FILES.getlist("frames")
    if len(frames) < 5:
        return JsonResponse({"success": False, "message": "Insufficient frames"})

    eye_states = []
    face_positions = []
    texture_scores = []

    for frame in frames:
        img_array = np.frombuffer(frame.read(), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5, minSize=(150, 150)
        )

        if len(faces) == 0:
            continue

        x, y, w, h = faces[0]
        face_positions.append((x, y, w, h))
        roi_gray = gray[y:y+h, x:x+w]

        # Eye detection
        eyes = eye_cascade.detectMultiScale(
            roi_gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30)
        )
        eye_states.append(len(eyes) >= 2)

        # Texture analysis (variance of Laplacian)
        texture = cv2.Laplacian(roi_gray, cv2.CV_64F).var()
        texture_scores.append(texture)

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

    return JsonResponse({
        "success": True,
        "message": "Liveness verified successfully"
    })
