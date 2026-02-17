from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

def search_members_api(request):
    print("hello")
    """
    API endpoint to search for users to assign as Club Members.
    Returns: JSON with 'results' list containing 'id' and 'text'.
    """
    query = request.GET.get('q', '').strip()
    
    # Only search if query length is sufficient (as per your JS logic)
    if len(query) >= 3:
        users = User.objects.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        ).distinct()[:10]  # Limit to top 10 results for performance
        
        results = [
            {
                'id': user.id, 
                'text': f"{user.username} - {user.get_full_name() if user.get_full_name() else user.username}"
            } 
            for user in users
        ]
        return JsonResponse({'results': results})
    
    return JsonResponse({'results': []})