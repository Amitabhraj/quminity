from functools import wraps
from django.shortcuts import redirect
from django.http import Http404
from Qapp.common import LEAD_ROLE, MODERATOR_USER_LIST,student_user,faculty_user
from Qapp.models import ClubMembership,Event

def check_privilege(user):
    return user.is_staff or user.user_type in MODERATOR_USER_LIST

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login/")
        return view_func(request, *args, **kwargs)
    return wrapper


def moderator_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login/")
        if request.user.user_type in MODERATOR_USER_LIST:
            return view_func(request, *args, **kwargs)
        else:
            raise Http404("Page not found") 
    return wrapper


def student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login/")
        if request.user.user_type == student_user:
            return view_func(request, *args, **kwargs)
        else:
            raise Http404("Page not found") 
    return wrapper



def faculty_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login/")
        if request.user.user_type == faculty_user:
            return view_func(request, *args, **kwargs)
        else:
            raise Http404("Page not found") 
    return wrapper



def is_associatedWithClub(view_func):
    """
    Decorator to check if user is associated with a club 
    or is privileged. Raises 404 if not. (Total 3 Conditions)
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect("/login/")

        is_privileged = check_privilege(user)
        
        club_membership_exist = ClubMembership.objects.filter(
            user=user,
            position__in=LEAD_ROLE
        )
        
        # Check conditions
        if not (is_privileged or club_membership_exist.exists() or user.faculty_assigned_club.exists()):
            raise Http404
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view



def is_associatedWithEvent(view_func):
    """
    Decorator to check if user is associated with any event or not,
    if user is not Associated with any Event then Raises 404. (4 Conditons)
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect("/login/")

        is_privileged = check_privilege(user)
        
        # We need club data to check if they are associated Event via a club
        club_membership_exist = ClubMembership.objects.filter(
            user=user,
            position__in=LEAD_ROLE
        )
        leader_club_ids = club_membership_exist.values_list('club_id', flat=True)
        associated_with_events = Event.objects.filter(club__in=leader_club_ids)
        
        # Check conditions
        if not (is_privileged or 
                user.faculty_assigned_event.exists() or 
                user.event_coordinator_event.exists() or 
                associated_with_events.exists()):
            raise Http404
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view