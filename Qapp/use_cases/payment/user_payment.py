from django.http import JsonResponse
import razorpay
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from Qapp.models import ClubEventPayment

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def create_payment(request,club,amount):
    amount = 10000
    
    payment = ClubEventPayment.objects.create(amount=amount)

    razorpay_order = client.order.create(dict(
        amount=amount,
        currency="INR",
        payment_capture=1
    ))

    payment.order_id = razorpay_order["id"]
    payment.save()

    context = {
        "order_id": razorpay_order["id"],
        "amount": amount,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
    }
    return render(request, "payment.html", context)



@csrf_exempt
def payment_success(request):
    import json
    data = json.loads(request.body)

    payment_id = data["razorpay_payment_id"]
    order_id = data["razorpay_order_id"]

    payment = ClubEventPayment.objects.get(order_id=order_id)
    payment.payment_id = payment_id
    payment.status = True
    payment.save()

    return JsonResponse({"status": "success"})