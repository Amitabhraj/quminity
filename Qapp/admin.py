from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Section,Course,Subject,Club

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("qid", "anonymous","section")}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Section)
admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(Club)