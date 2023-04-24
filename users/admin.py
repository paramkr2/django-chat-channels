from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'full_name', 'phone', 'gender', 'country', 'status','busy')
    fieldsets = (
        (None, {'fields': ('username', 'password','status','busy')}),
        ('Personal info', {'fields': ('full_name', 'email', 'phone', 'gender', 'country')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Additional Info', {'fields': ('interests',)})
    )
    

admin.site.register(User, CustomUserAdmin)





