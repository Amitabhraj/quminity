from Qapp.models import ActiveToken, Club
from Qapp.qr_code.common import check_club_core_member
import jwt
from django.shortcuts import render,redirect
import datetime
import qrcode
import base64
import time
from io import BytesIO
from django.http import JsonResponse
from django.conf import settings
from datetime import timedelta
from django.utils import timezone


# Load config from settings.py
SECRET_KEY = settings.QR_SECRET_KEY
ALGO = settings.QR_JWT_ALGO
TOKEN_TTL = settings.QR_TOKEN_TTL
EVENT_ID = settings.QR_EVENT_ID


def GenerateQR(request,club_id):
    success, event_or_club = check_club_core_member(request,club_id)
    if not success:
        return redirect("/")
    
    payload = {
        "event": EVENT_ID,
        "role": "student_attendance",
        "iat": int(time.time()),
        "exp": int(time.time()) + TOKEN_TTL
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGO)

    qr = qrcode.QRCode(
        version=1,
        box_size=15,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        border=4
    )
    qr.add_data(token)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white") 

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    expires_at = timezone.now() + timedelta(seconds=TOKEN_TTL)

    ActiveToken.objects.create(token=token,event_or_club=event_or_club, expires_at=expires_at)

    return JsonResponse({
        "qr": qr_base64,
        "token": token,
        "expires_in": TOKEN_TTL
    })