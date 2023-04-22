from django.contrib import admin

from chat.models import Room, Message , Requests

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Requests)
