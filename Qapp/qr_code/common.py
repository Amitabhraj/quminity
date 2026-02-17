from Qapp import models
from Qapp.common import LEAD_ROLE, MODERATOR_USER_LIST
from Qapp.models import Club, ClubMembership, Event
from django.db.models import Q

def get_user_associations(user):
########
    is_privileged = False
    if user.is_staff or user.user_type in MODERATOR_USER_LIST:
        is_privileged = True
########


########
    is_associated_with_club = False
    club_membership_exist = ClubMembership.objects.filter(
                                                    user=user,
                                                    position__in=LEAD_ROLE
                                                    )
    if is_privileged or club_membership_exist.exists() or user.faculty_assigned_club.exists():
        is_associated_with_club = True
########


########
    is_associated_with_event = False
    leader_club_ids = club_membership_exist.values_list('club_id', flat=True)
    associated_with_club_events = Event.objects.filter(club_id__in=leader_club_ids)
    if is_privileged or user.faculty_assigned_event.exists() or user.event_coordinator_event.exists() or associated_with_club_events:
        is_associated_with_event = True
########

    return is_associated_with_club, is_associated_with_event

def check_club_core_member(request,club_id):
    usr_obj = request.user
    try:
        event_or_club = Club.objects.get(id=club_id,core_members=usr_obj)
    except Club.DoesNotExist:
        return False, "Club Does not Exists or Core Member is not associated with this club"
    
    return True, event_or_club