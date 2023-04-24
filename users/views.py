from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import CustomUserCreationForm
# Create your views here.

from django.shortcuts import render


def register(request):
	if request.method == "GET":
		return render(
			request, "users/register.html",
			{"form": CustomUserCreationForm}
		)
	elif request.method == "POST":
		form = CustomUserCreationForm(request.POST)
		#form.add_error('username', 'This is a test error message.')
		if form.is_valid():
			interests = form.cleaned_data.get('interests')
			user = form.save()
			user.interests.set(interests)
			user.save()
			login(request, user)
			return redirect(reverse("chat:chat-room"))
		else:
			return render(
				request, "users/register.html",
				{"form": form}
			)
