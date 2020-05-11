from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render


def home(request):
	return redirect('chatroom:lobby')


def login_view(request):
	"""
	Function to manage user's authentication
	:return: A render of login page
	"""
	error = False
	if request.method == "POST":
		username = request.POST["username"]
		raw_password = request.POST["password"]
		user = authenticate(username=username, password=raw_password)
		if user is not None:
			login(request, user)
			return redirect('chatroom:lobby')
		error = True
	context = {
		'title': 'Chat Rooms',
		'error': error
	}
	return render(request, "login.html", context)


def logout_view(request):
	"""
	Function to logout from session
	:return: A render of login page
	"""
	auth.logout(request)
	return render(request, 'login.html')
