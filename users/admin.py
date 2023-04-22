from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'full_name', 'phone', 'gender', 'country')
    fieldsets = UserAdmin.fieldsets 
    


admin.site.register(User, CustomUserAdmin)