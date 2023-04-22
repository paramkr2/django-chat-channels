from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from chat.models import Room
from users.models import User


def index_view(request):
	return render(request, 'index.html', {
		'rooms': Room.objects.all(),
	})

@never_cache
def room_view(request, room_name):
	return render(request, 'room.html', {
		'room': room_name,
	})
@login_required
def dashboard(request):
	status = User.objects.all().filter(id=request.user.id)
	context = { 'status':status } 
	return render(request,"dashboard.html" );
	