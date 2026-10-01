from django.shortcuts import render

def ScanEventAttendanceQr(request):
    return render(request, "QrCode/QrScan.html")