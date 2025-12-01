from django.shortcuts import render


def instructor_page(request):
    """
    Page where instructor can click button to get QR Code.
    Frontend uses /api/instructor_qr/ to fetch QR.
    """
    return render(request, "html/QRCode/instructorQR.html")


def scan_page(request):
    """
    Student camera page to scan QR code.
    Camera permission + JS scanner works here.
    """
    return render(request, "html/QRCode/studentScan.html")
