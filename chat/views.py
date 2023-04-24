from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from chat.models import Room,ChatRoom
from users.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction
@login_required
@never_cache
def room_view(request):
	print(f'room_view called ');
	
	if request.method == 'POST':
		if( 'status' in request.POST ):
			button_value = request.POST.get('status')
			if button_value == 'off':
				request.user.status = True 
			elif button_value == 'on':
				request.user.status = False 
			request.user.save()
			
	context = { 'status':request.user.status  } 
	return render(request, 'room.html', context)

@never_cache
@login_required
@csrf_exempt	
def get_room(request):
	if request.method == 'POST':
		# first check in room 
		re = ChatRoom.objects.filter(user=request.user.id).first();
		if( re is not None  ):
			print(f'room already exists {re}')
			room_name = f'{min(request.user.id, re.receiver.id)}_{max(request.user.id, re.receiver.id)}'
			receiver = re.receiver
			#room_name  = f'{min(request.user.id,re.receiver.id)}_{max(request.user.id,re.receiver.id)}'
			# also get other details later 
			with transaction.atomic():
				re.delete()
		else:	
			# fetch and connect 
			print( 'in getroom| printing user interests', list( request.user.interests.all().values_list('name',flat=True)) ) # will return a user object with the attributes attached , not a queryset 	
			interests = list( request.user.interests.all().values_list('id',flat=True))
			
			# user in online and not busy and in interestlist, and also not already being connected to 
			users = User.objects.all().exclude(id=request.user.id).exclude(
				id__in = list(ChatRoom.objects.all().values_list('user',flat=True))
			).filter(status=True,busy=False, interests__in = interests )
			
			if( len(users)==0 ):
				users = User.objects.all().exclude(id=request.user.id ).exclude(
					id__in = list(ChatRoom.objects.all().values_list('user',flat=True))
				).filter(status=True,busy=False)
				if(len(users) == 0 ):
					return JsonResponse({ 'details':{} , 'valid':False }) 
			# make the current user busy 
			request.user.busy = True
			request.user.save()
			# pick the first one 
			receiver = users[0]
			room_name = f'{min(request.user.id,receiver.id)}_{max(request.user.id,receiver.id)}'
			room_obj = ChatRoom(user=receiver,receiver = request.user )
			room_obj.save()
			#request.user.busy.set(True) # make the user busy 
		
		return JsonResponse({ 
			'details':{
				'room_name':room_name , 
				'userinfo':{ 
					'username': receiver.username ,
					'gender':receiver.gender,
					'country':receiver.country,
				}
			},
			'valid':True 
		})
	
	
@csrf_exempt
@login_required
def set_user_offline(request):
	user = request.user
	user.status = False
	user.busy = False 
	user.save()
	# delete any chatroom where he is the receiver  
	re = ChatRoom.objects.filter(receiver=request.user.id).first();
	if( re is not None):
		with transaction.atomic():
			re.delete()
	
	return JsonResponse({'success': 'User status updated to False'})
	