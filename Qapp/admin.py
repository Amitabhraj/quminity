from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("qid",
                                        "anonymous",
                                        "face_encoding",
                                        'user_type',
                                        'country_code_for_mobile',
                                        'mobile',
                                        'program',
                                        'branch',
                                        'section',
                                        'current_year',
                                        'registration_number',
                                        'registered_at',
                                        'updated_at')}),
    )
admin.site.register(Attendance)
admin.site.register(ActiveToken)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Section)
admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(Club)
admin.site.register(Event)
admin.site.register(EventPayment)
admin.site.register(ClubPayment)
admin.site.register(Notification)
admin.site.register(ClassRoom)
admin.site.register(PendingUser)
