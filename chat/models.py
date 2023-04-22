from users.models import User
from django.db import models


class Room(models.Model):
	name = models.CharField(max_length=128)
	online = models.ManyToManyField(to=User, blank=True)
	
	def get_online_count(self):
		return self.online.count()

	def join(self, user):
		self.online.add(user)
		self.save()

	def leave(self, user):
		self.online.remove(user)
		self.save()

	def __str__(self):
		return f'{self.name} ({self.get_online_count()})'

class Message(models.Model):
	room = models.ForeignKey(Room, related_name='chat_room', on_delete=models.CASCADE)
	user = models.ForeignKey(User, related_name='user_msg', on_delete=models.CASCADE)
	message = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-timestamp']
		
class Requests(models.Model):
	# this will lead us to connect to the room 
	sender = models.ForeignKey(User, related_name='req_sender', on_delete=models.CASCADE)
	