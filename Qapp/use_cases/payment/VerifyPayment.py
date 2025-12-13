import json
from django.http import JsonResponse
import razorpay
from Qapp.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from Qapp.models import CustomUser
from Qapp.use_cases.payment.GetPayment_orderID import GetPayment
from quminity.settings import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

"""
This Function Verify the Payment Which is done by User ......!
"""

@csrf_exempt
@login_required
def VerifyPayment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        razorpay_order_id = data['razorpay_order_id']
        razorpay_payment_id = data['razorpay_payment_id']
        razorpay_signature = data['razorpay_signature']

        paymentDetail = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        }

        try:
            # Razorpay's OFFICIAL method
            Payment_IsDone = client.utility.verify_payment_signature(paymentDetail)
            if Payment_IsDone:
                result = GetPayment(request,paymentDetail['razorpay_order_id']) #Get Payment Object of provided Order-Id
                payment_obj = result['payment']
                payment_obj.payment_id = paymentDetail['razorpay_payment_id']
                payment_obj.status = True
                club_obj = payment_obj.club
                event_obj = payment_obj.event
                if club_obj:
                    club_obj.student_enrolled.add(user_obj)
                    club_obj.save()
                elif event_obj:
                    event_obj.student_enrolled.add(user_obj)
                    event_obj.save()
                else:
                    return JsonResponse({"message": "Some Error Occured !! Contact Coordinator","status":400})
                user_obj = CustomUser.objects.get(id=request.user.id)
                payment_obj.save()
            else:
                return JsonResponse({"message": "Payment Failed","status":400})
                    
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"message": "Payment Failed / System Error !!! Contact Coordinator","status":400})

    return JsonResponse({"message": "invalid method","status":400})

