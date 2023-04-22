# users/forms.py

from django.contrib.auth.forms import UserCreationForm
from django import forms 
from users.models import Interest,User


class CustomUserCreationForm(UserCreationForm):
	interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'list-unstyled'}),
        required=True,
    )
	status = forms.BooleanField(widget=forms.HiddenInput(), initial=False,label='')
	def __init__(self, *args, **kwargs):
		super(CustomUserCreationForm, self).__init__(*args, **kwargs)
		for name, field in self.fields.items():
			#if field.widget.__class__ == forms.widgets.TextInput:
			if 'class' in field.widget.attrs:
				field.widget.attrs['class'] += 'input'
			else:
				field.widget.attrs.update({'class':'input'})
			
			print(name)
	class Meta(UserCreationForm.Meta):
		model = User
		fields = UserCreationForm.Meta.fields + ("email","full_name","phone","gender","country","interests")