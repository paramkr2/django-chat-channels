from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message,User,Requests,Room
class ChatConsumer(WebsocketConsumer):

	def __init__(self, *args, **kwargs):
		super().__init__(args, kwargs)
		self.room_name = None
		self.room_group_name = None
		self.room = None
		self.active_user = [] 
		
	def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room']
		#self.room_group_name = f'chat_{self.room_name}'
		self.u_list = list(map(int, self.room_name.split('_') ) )
		self.user = self.scope['user']
		self.receiver = self.u_list[1] if self.u_list[0] == self.user.id else self.u_list[0] 
		self.room,_ = Room.objects.get_or_create(name = self.room_name) 
		self.room.online.add(self.user.id ) 
		print(f'user:{self.user}')
		if self.user.id  not in self.u_list:
			print(f'Un-Authorized')
			return
		# connection has to be accepted
		self.accept()

		# Fetch the data
		latest_messages = list(Message.objects.select_related('user').order_by(
			'-timestamp'
		).filter(
			room=self.room 
		).values_list( 
			'user__username','message','timestamp' 
		))
		latest_messages.reverse()
		initial_msgs = []
		for msg in latest_messages[:10]:
			initial_msgs.append(
				{ 
					'user':msg[0] ,
					'msg':msg[1],
				}
			)
		# join the room group
		async_to_sync(self.channel_layer.group_add)(
			self.room_name,
			self.channel_name,
		)
		self.send(text_data=json.dumps({'type': 'initial_msgs','msgs':initial_msgs}))


	def disconnect(self, close_code):
		self.user.busy = False
		self.user.save()
		self.room.online.remove(self.user.id )
		

	def receive(self, text_data=None, bytes_data=None):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		
		# save msg 
		message_obj = Message(room=self.room , user=User(self.user.id ), message=message) 
		message_obj.save()
		'''
		# add msg to requests, if receiver is not connected 
		active_users = list(self.room.online.all().values_list('id' , flat=True ))
		if( self.receiver not in active_users ):
			req,created = Requests.objects.get_or_create( sender=User(self.user.id ) ) #remove this while accessing 
			print(f'Request object created:{created} {req}')
		'''	
		# send chat message event to the room
		async_to_sync(self.channel_layer.group_send)(
			self.room_name,
			{
				'type': 'chat_message',
				'user': self.user.username  ,
				'message': message,
			}
		)

	def chat_message(self, event):
		self.send(text_data=json.dumps(event))
