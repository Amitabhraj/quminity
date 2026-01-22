from django.core.paginator import Paginator
from Qapp.models import Attendance

# Queryset (optimized)
attendance_qs = (
    Attendance.objects
    .filter(event=event)
    .select_related('student')
    .order_by('-attendance_marked_at')
)

# Pagination
paginator = Paginator(attendance_qs, 10)  # 10 students per page
page_number = request.GET.get('page', 1)
attendance = paginator.get_page(page_number)
