from Qapp.models import ActiveToken, Attendance
import jwt
import json
from django.utils import timezone
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


SECRET_KEY = settings.QR_SECRET_KEY
ALGO = settings.QR_JWT_ALGO
EVENT_ID = settings.QR_EVENT_ID

@csrf_exempt
def validate_attendance(request):
    data = json.loads(request.body)
    token = data.get("token")
    student_id = request.user.qid

    if not token:
        return JsonResponse({"status": "error", "message": "Token or Student ID missing"}, status=400)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        
        if not ActiveToken.objects.filter(token=token, expires_at__gt=timezone.now()).exists():
            return JsonResponse({"status": "error", "message": "QR Expired"}, status=400)

        Attendance.objects.create(
            student_id=student_id,
            ip_address=request.META.get('REMOTE_ADDR'),
            event_or_club = 
            )

        return JsonResponse({
            "status": "success",
            "message": f"Attendance marked for {student_id}",
            "payload": payload,
        })

    except jwt.ExpiredSignatureError:
        return JsonResponse({"status": "expired", "message": "QR expired"}, status=401)

    except jwt.InvalidTokenError:
        return JsonResponse({"status": "invalid", "message": "Invalid QR"}, status=401)