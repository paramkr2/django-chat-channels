from django.urls import path

from . import views
app_name = 'chat'
urlpatterns = [
    #path('', views.index_view, name='chat-index'),
	path('get_room/',views.get_room,name='get_room'),
	path('set_user_offline/',views.set_user_offline, name='set_user_offline'),
    path('', views.room_view, name='chat-room'),
]
