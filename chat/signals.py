from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_delete
from django.dispatch import receiver

@receiver(pre_delete, sender=Session)
def end_session(sender, instance, **kwargs):
	print(f'Ending Session')
	user_id = instance.get_decoded().get('_auth_user_id')
	if user_id:
		User = get_user_model()
		user = User.objects.get(id=user_id)
		user.status = False
		user.save()