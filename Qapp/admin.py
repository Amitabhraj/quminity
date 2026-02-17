from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Qapp.models import *

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
    readonly_fields = ('face_encoding',)

class ClubAdmin(admin.ModelAdmin):
    list_display = ('club_name','entry_fees', 'active', 'created_at', 'updated_at')
    list_filter = ('active', 'created_at')
    search_fields = ('club_name', 'description')
    readonly_fields = ('created_at', 'updated_at','members')


admin.site.register(Attendance)
admin.site.register(ActiveToken)
admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Section)
admin.site.register(Subject)
admin.site.register(StudentEventEnrolled)
admin.site.register(Course)
admin.site.register(Club,ClubAdmin)
admin.site.register(Event)
admin.site.register(ClubMembership)
admin.site.register(EventPayment)
admin.site.register(ClubPayment)
admin.site.register(Notification)
admin.site.register(ClassRoom)
admin.site.register(PendingUser)
