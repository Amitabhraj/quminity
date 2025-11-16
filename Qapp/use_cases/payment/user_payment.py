from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from quminity.settings import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
import razorpay
import json
from Qapp.models import ClubEventPayment


client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


def club_payment(request, Id, clubName, entryFee):
    entryFee = entryFee * 100
    return create_payment(request, clubName, entryFee)


def create_payment(request, clubId, clubName, amount):

    payment = ClubEventPayment.objects.create(amount=amount)

    razorpay_order = client.order.create(dict(
        amount=amount*100,
        currency="INR",
        payment_capture=1
    ))

    try:
        club_obj = ClubEventPayment.objects.get(id=payment.id)
    except ClubEventPayment.DoesNotExist:
        return redirect("/")

    payment.order_id = razorpay_order["id"]
    payment.event_or_club = club_obj
    payment.save()

    context = {
        "order_id": razorpay_order["id"],
        "amount": amount,
        "razorpay_key": RAZORPAY_KEY_ID,
    }
    return render(request, "html/dashboard/payment.html", context)



@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = json.loads(request.body)

        payment_id = data["razorpay_payment_id"]
        order_id = data["razorpay_order_id"]

        payment = ClubEventPayment.objects.get(order_id=order_id)
        payment.payment_id = payment_id
        payment.status = True
        payment.save()

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "invalid method"})




def payment_done(request, order_id):
    try:
        payment = ClubEventPayment.objects.get(order_id=order_id)
        status = payment.status
    except ClubEventPayment.DoesNotExist:
        status = False
    return render(request, "html/dashboard/paymentDone.html", {"payment": payment,'status': status})