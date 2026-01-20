from django.shortcuts import render

def ScanEventAttendanceQr(request):
    return render(request, "html/QrCode/QrScan.html")