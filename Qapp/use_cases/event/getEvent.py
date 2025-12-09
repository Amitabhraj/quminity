from Qapp.models import Event

def GetEvent(eventId):
    try:
        event = Event.objects.get(id=eventId)
        return {'redirect':False,'event_obj':event}
    except:
        return {'redirect':True,'event_obj':None}