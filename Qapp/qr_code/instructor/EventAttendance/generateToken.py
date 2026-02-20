from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
import jwt
import qrcode
import base64
import time
from io import BytesIO
from django.http import Http404, JsonResponse
from django.conf import settings
from Qapp.models import ActiveToken, Event

def GenerateQR(request, EventId):
    if not Event.objects.is_user_associated_with_provided_event(request.user, EventId):
        raise Http404
    
    event = get_object_or_404(Event, id=EventId)

    # 2. Use settings with fallbacks to prevent NoneType errors
    SECRET_KEY = getattr(settings, 'QR_SECRET_KEY', 'fallback-secret')
    ALGO = getattr(settings, 'QR_JWT_ALGO', 'HS256')
    TOKEN_EXPIRY = getattr(settings, 'QR_TOKEN_EXPIRY', 300)

    # 3. JWT payload (Use the dynamic event.id, not the hardcoded one)
    payload = {
        "event_id": str(EventId), 
        "role": "student_attendance",
        "iat": int(time.time()),
        "exp": int(time.time()) + TOKEN_EXPIRY,
    }

    try:
        # Generate token
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGO)

        # 4. QR Code Generation
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
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