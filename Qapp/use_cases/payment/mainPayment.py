import razorpay
from Qapp.models import Club, ClubPayment, Event,EventPayment
from quminity.settings import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

def CreatePayment(request,clubId,eventId):  # Creating Event or Club Payment OBJECT
    user_obj = request.user
  
    if clubId:
        club=Club.objects.get(id=clubId)
        payment = ClubPayment.objects.create(student=user_obj,club=club,amount=club.entry_fees,status=False)
    elif eventId:
        event=Event.objects.get(id=clubId)
        payment = EventPayment.objects.create(student=user_obj,event=event,amount=event.entry_fees,status=False)

    razorpay_order = client.order.create(dict(amount=payment.amount*100,currency="INR",payment_capture=1))
    payment.order_id = razorpay_order["id"]
    payment.save()

    context = {
        "payment":payment,
        "razorpay_key": RAZORPAY_KEY_ID,
    }
    return context