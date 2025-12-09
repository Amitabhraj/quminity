from django.http import JsonResponse
from django.shortcuts import render
from Qapp.decorators import login_required
from Qapp.use_cases.payment.GetPayment_orderID import GetPayment


@login_required
def PaymentStatus(request, order_id):
    result = GetPayment(request,order_id) # Get Payment Details with Order-id from Database for Verification
    payment_obj = result['payment'] # Payment Object

    if result['redirect']:
        return JsonResponse({"message":result['message']})
    
    return render(request,"html/dashboard/paymentStatus.html",{"payment":payment_obj})