import cv2
import numpy as np
import base64
import jwt
from pyzbar.pyzbar import decode
from django.utils import timezone
from django.http import JsonResponse
from django.conf import settings
from Qapp.decorators import login_required
from Qapp.models import ActiveToken, Attendance, StudentEventEnrolled
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def validate_attendance(request):
    frame_data = request.POST.get("frame")
    student = request.user

    if not frame_data:
        return JsonResponse({"status": "searching", "message": "FINDING THE QR...."})

    try:
        # 1. Decode the Base64 frame
        format, imgstr = frame_data.split(';base64,')
        img_data = base64.b64decode(imgstr)
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # 2. Detect QR code using PyZbar
        qr_codes = decode(img)
        print(qr_codes)
        if not qr_codes:
            return JsonResponse({"status": "searching", "message": "FINDING THE QR...."})

        # 3. Get Token from first detected QR
        token = qr_codes[0].data.decode('utf-8')

        # 4. Use your existing logic for JWT & Attendance
        try:
            payload = jwt.decode(token, settings.QR_SECRET_KEY, algorithms=[settings.QR_JWT_ALGO])

            token_obj = ActiveToken.objects.get(
                current_token=token, 
                expires_at__gt=timezone.now()
            )
            
            event = token_obj.event
            if event.id != int(payload.get("event_id")):
                return JsonResponse({"status": "error", "message": "INVALID EVENT QR"})
            
            # Check if already marked
            if Attendance.objects.filter(student=student, event=event, is_present=True).exists():
                return JsonResponse({"status": "success", "message": "Attendance already marked"})
            
            if not StudentEventEnrolled.objects.filter(event=event,status=True,student_enrolled=student).exists():
                return JsonResponse({"status": "error", "message": "You are not Part of This Event ! Kindly Join the Event before marking Attendance."})

            # Create record
            Attendance.objects.create(
                student=student,
                event=event,
                attendance_marked_at=timezone.now(),
                is_present=True
            )
            
            return JsonResponse({"status": "success", "message": f"Attendance Successfully Marked for QID: {student.qid}"})

        except jwt.ExpiredSignatureError:
            return JsonResponse({"status": "expired", "message": "QR EXPIRED"}, status=200)
        except (jwt.InvalidTokenError, ActiveToken.DoesNotExist):
            return JsonResponse({"status": "error", "message": "INVALID OR EXPIRED"}, status=200)

    except Exception as e:
        print(f"Error processing frame: {e}")
        return JsonResponse({"status": "searching", "message": "FINDING THE QR...."})