from django.urls import path

from . import views
app_name = 'chat'
urlpatterns = [
    #path('', views.index_view, name='chat-index'),
	path('' , views.dashboard, name='dashboard'),
    path('chat/<str:room_name>/', views.room_view, name='chat-room'),
]
