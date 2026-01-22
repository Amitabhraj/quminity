import cv2
from django.http import JsonResponse
import numpy as np
import pickle
import face_recognition
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Qapp.models import CustomUser
from Qapp.use_cases.user_onboarding.face_login.match_face import match_face
from Qapp.use_cases.user_onboarding.logout_user import user_logout
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def face_login(request):
    image_file = request.FILES.get("image")
    if not image_file:
        return Response(
            {"success": False, "message": "Image not received"},
            status=400
        )

    # 🔹 Read bytes
    image_bytes = image_file.read()
    if not image_bytes:
        return Response(
            {"success": False, "message": "Empty image"},
            status=400
        )

    # 🔹 Decode image safely
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        return Response(
            {"success": False, "message": "Invalid image format"},
            status=400
        )

    # 🔹 Ensure uint8
    if img.dtype != np.uint8:
        img = img.astype(np.uint8)

    # 🔹 Convert BGR → RGB
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 🔹 Face detection
    face_locations = face_recognition.face_locations(rgb_img, model="hog")

    if len(face_locations) == 0:
        return Response(
            {"success": False, "message": "No face detected"},
            status=400
        )

    # 🔹 Face encoding
    face_encodings = face_recognition.face_encodings(rgb_img, face_locations)

    if not face_encodings:
        return Response(
            {"success": False, "message": "Face encoding failed"},
            status=400
        )

    incoming_encoding = face_encodings[0]

    result = match_face(request.user.face_encoding, incoming_encoding)

    if result:
        print("Face matched successfully")
        return JsonResponse(
            {"success": True, "message": "Face recognized, logged in successfully"}
        )

    return Response(
        {"success": False, "message": "Face not recognized"},
        status=401
    )
