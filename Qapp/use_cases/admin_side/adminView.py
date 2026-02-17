from django.shortcuts import render
from Qapp.decorators import login_required,moderator_required
from Qapp.qr_code.common import get_user_associations

@login_required
@moderator_required
def MainView(request):
    user = request.user
    response = get_user_associations(user)
    print(response)
    return render(request, 'html/dashboard/moderator_dashboard.html') 