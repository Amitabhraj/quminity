# views.py
import cv2
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

@csrf_exempt
def DetectFace(request):
    if request.method != "POST":
        return JsonResponse({"success": False})

    image_file = request.FILES.get("image")
    if not image_file:
        return JsonResponse({"success": False})

    image_bytes = image_file.read()
    np_img = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        return JsonResponse({
            "success": True,
            "message": "Face detected"
        })

    return JsonResponse({"success": False})
