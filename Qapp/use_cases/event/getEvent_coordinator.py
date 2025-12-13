from Qapp.models import Event

def check_event_coordinator(request,eventId):
    usr_obj = request.user
    try:
        event = Event.objects.get(id=eventId,event_coordinator=usr_obj)
        return event
    except:
        return False