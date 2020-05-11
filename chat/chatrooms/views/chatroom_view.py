from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
from chatrooms.models import Chatroom


@login_required(login_url='/login')
def lobby(request):
	# Get all chat rooms saved
	chat_rooms = Chatroom.objects.all()
	context = {
		'title': 'Chat Rooms',
		'chat_rooms': chat_rooms
	}
	return render(request, 'chatrooms/lobby.html', context)


@login_required(login_url='/login')
def room(request, name):
	# Check if room exists or create it
	chat_room = Chatroom.objects.filter(name=name).first()
	if not chat_room:
		chat_room = Chatroom.objects.create(
			name=name
		)
	context = {
		'title': 'Chat Room - ' + chat_room.name,
		'chat_room': chat_room.name,
		'username': request.user.username
	}
	return render(request, 'chatrooms/room.html', context)
