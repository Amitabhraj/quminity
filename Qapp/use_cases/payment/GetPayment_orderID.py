from Qapp.models import ClubPayment, EventPayment

"""
This Function Filter Payment Object with Order ID and return Some Paramenters in 
JSON Format
"""

def GetPayment(request,order_id):
    try:
        payment = EventPayment.objects.get(order_id=order_id)
        redirect,message = False,"Event Payment Details Retrieved"
    except:
        try:
            payment = ClubPayment.objects.get(order_id=order_id)
            redirect,message = False,"Club Payment Details Retrieved"
        except:
            payment = None
            redirect,message = True,"No Payment Found !!! Contact Coordinator"
    
    if payment:
        if request.user != payment.student:
            redirect = True
            redirect,message = True,"Can't Access"
            
    response = {
        'redirect':redirect,
        'payment':payment,
        'message':message
    }
    return response