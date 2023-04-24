from django.db import models
from django.contrib.auth.models import AbstractUser 

class Interest(models.Model):
	Interest_Choices = [
		('F', 'Footbal'),
		('H', 'Hockey'),
	]
	name = models.CharField(max_length=1,choices=Interest_Choices)
	def __str__(self):
		return self.name

class User(AbstractUser):
	full_name = models.CharField(max_length=255)
	email = models.EmailField(unique=True)
	phone = models.CharField(max_length=20)
	GENDER_CHOICES = [
		('M', 'Male'),
		('F', 'Female'),
		('O', 'Other'),
	]
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	country = models.CharField(max_length=255)
	interests = models.ManyToManyField('Interest')
	status = models.BooleanField(default=False)
	busy = models.BooleanField(default=False)
	
	def __str__(self):
		return self.email
		
