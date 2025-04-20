from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")
    fieldsets = UserAdmin.fieldsets + (("CRM Role", {"fields": ("role",)}),)


admin.site.register(User, CustomUserAdmin)
