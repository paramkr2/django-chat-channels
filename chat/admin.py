from django.contrib import admin

from chat.models import Room, Message , Requests,ChatRoom
from django.contrib.sessions.models import Session
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Requests)
admin.site.register(ChatRoom)

class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'session_data', 'expire_date')

admin.site.register(Session, SessionAdmin)
