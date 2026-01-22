import cv2
import numpy as np
import face_recognition
import pickle
from PIL import Image
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from quminity.settings import BASE_DIR


# ==========================
# LOAD HAAR CASCADES
# ==========================
face_cascade = cv2.CascadeClassifier(
    str(BASE_DIR / "haarcascade_frontalface_default.xml")
)
eye_cascade = cv2.CascadeClassifier(
    str(BASE_DIR / "haarcascade_eye_tree_eyeglasses.xml")
)


# ==========================
# SAFE IMAGE CONVERSION (CRITICAL)
# ==========================
def to_safe_rgb(bgr_image):
    """
    Converts OpenCV BGR image into a guaranteed-safe
    uint8 RGB numpy array for dlib / face_recognition
    """
    rgb = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)
    pil_img = pil_img.convert("RGB")   # strips alpha, metadata, profiles
    safe_rgb = np.array(pil_img, dtype=np.uint8)
    return safe_rgb


# Load Haar Cascades
face_cascade = cv2.CascadeClassifier(
    str(BASE_DIR / "haarcascade_frontalface_default.xml")
)
eye_cascade = cv2.CascadeClassifier(
    str(BASE_DIR / "haarcascade_eye_tree_eyeglasses.xml")
)

@csrf_exempt
def register_face(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "Login required"}, status=401)

    frames = request.FILES.getlist("frames")
    if len(frames) < 5:
        return JsonResponse({"success": False, "message": "Insufficient frames"})

    eye_states = []
    face_positions = []
    texture_scores = []
    valid_encodings = []

    for frame in frames:
        img_array = np.frombuffer(frame.read(), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if img is None:
            continue

        # Ensure correct format
        img = np.ascontiguousarray(img, dtype=np.uint8)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # ---- FACE DETECTION (HAAR) ----
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(150, 150)
        )

        if len(faces) == 0:
            continue

        x, y, w, h = faces[0]
        face_positions.append((x, y, w, h))

        # ---- LIVENESS CHECKS ----
        roi_gray = gray[y:y+h, x:x+w]
        roi_rgb = rgb[y:y+h, x:x+w]

        # Texture (anti-spoof)
        texture_scores.append(cv2.Laplacian(roi_gray, cv2.CV_64F).var())

        # Eye detection (blink)
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
        eye_states.append(len(eyes) >= 2)

        # ---- FACE ENCODING (CORRECT WAY) ----
        try:
            encodings = face_recognition.face_encodings(
                roi_rgb,
                known_face_locations=[(0, w, h, 0)],  # FULL ROI
                num_jitters=2
            )
            if encodings:
                valid_encodings.append(encodings[0])
        except Exception:
            continue

    # ---- FINAL VALIDATION ----
    if len(valid_encodings) < 1 or len(face_positions) < 3:
        return JsonResponse({
            "success": False,
            "message": "Face detected but encoding failed."
        })

    # Motion check
    motion = any(
        abs(face_positions[i][0] - face_positions[i-1][0]) > 5
        for i in range(1, len(face_positions))
    )

    # Texture check
    avg_texture = np.mean(texture_scores)

    # Blink check
    blink_detected = False
    for i in range(1, len(eye_states) - 1):
        if eye_states[i-1] and not eye_states[i] and eye_states[i+1]:
            blink_detected = True
            break

    if not motion:
        return JsonResponse({"success": False, "message": "No movement detected"})
    if avg_texture < 30:
        return JsonResponse({"success": False, "message": "Spoof detected"})
    if not blink_detected:
        return JsonResponse({"success": False, "message": "Blink not detected"})

    # ---- SAVE FACE ----
    user = request.user
    user.face_encoding = pickle.dumps(valid_encodings[0])
    user.save()

    return JsonResponse({
        "success": True,
        "message": "Face registered successfully"
    })
