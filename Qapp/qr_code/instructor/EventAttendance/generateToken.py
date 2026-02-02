from django.utils import timezone
from datetime import timedelta
import jwt
import qrcode
import base64
import time
from io import BytesIO
from django.http import JsonResponse
from django.conf import settings
from Qapp.models import ActiveToken
from Qapp.use_cases.event.getEvent_coordinator import check_event_coordinator

def GenerateQR(request, eventId):
    # 1. Validate Coordinator (Ensure eventId matches URL param)
    event = check_event_coordinator(request, eventId)
    if not event:
        return JsonResponse({"status": "error", "message": "Unauthorized or Event not found"}, status=403)

    # 2. Use settings with fallbacks to prevent NoneType errors
    SECRET_KEY = getattr(settings, 'QR_SECRET_KEY', 'fallback-secret')
    ALGO = getattr(settings, 'QR_JWT_ALGO', 'HS256')
    TOKEN_EXPIRY = getattr(settings, 'QR_TOKEN_EXPIRY', 300)

    # 3. JWT payload (Use the dynamic event.id, not the hardcoded one)
    payload = {
        "event_id": str(event.id), 
        "role": "student_attendance",
        "iat": int(time.time()),
        "exp": int(time.time()) + TOKEN_EXPIRY,
    }

    try:
        # Generate token
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGO)

        # 4. QR Code Generation
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=15,
            border=4
        )
        qr.add_data(token)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()

        # 5. Database Update (update_or_create is cleaner)
        expires_at = timezone.now() + timedelta(seconds=TOKEN_EXPIRY)
        
        ActiveToken.objects.update_or_create(
            event=event,
            defaults={
                "current_token": token,
                "expires_at": expires_at,
                "created_at": timezone.now() # Ensure this field exists in Models
            }
        )

        return JsonResponse({
            "status": "success",
            "qr": qr_base64,
            "token": token,
            "expires_in": TOKEN_EXPIRY
        })

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)