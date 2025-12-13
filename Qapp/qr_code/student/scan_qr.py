from django.shortcuts import render

def scan_attendance_qr(request):
    return render(request, "html/QrCode/QrScan.html")