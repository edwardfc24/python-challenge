import json

from channels.generic.websocket import AsyncWebsocketConsumer

from base.repositories.message_repository import MessageRepository
from bot.services import BotService
from chatrooms.models import User, Chatroom


class ChatroomConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = 'chat_%s' % self.room_name
		self.message_repository = MessageRepository()
		self.bot = BotService()
		# Join room group
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		await self.accept()

	async def disconnect(self, close_code):
		# Leave room group
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	# Receive message from WebSocket
	async def receive(self, text_data):
		data = json.loads(text_data)
		self.COMMANDS[data['command']](self, data)



	def create_message(self, message_obj):
		# Retrieve the user
		user = User.objects.filter(username=message_obj['author']).first()
		# Retrieve the room
		room = Chatroom.objects.filter(name=self.room_name).first()
		# Validate if coe is present in message
		if '/' in message_obj['message']:
			message = self.message_repository.create_message(room, user, message_obj['message'], False)
			self.send_message(message)
			command, code = self.get_command_code(message_obj['message'])
			self.bot.bot_response(room, command, code)
		else:
			message = self.message_repository.create_message(room, user, message_obj['message'])
			self.send_message(message)

	def message_list(self, message_obj):
		messages = self.message_repository.get_last_messages_for_room(self.room_name)
		content = {
			'command': 'list',
			'type': 'chat.message',
			'message': messages
		}
		self.send_message(content)

	# CONSTANTS
	COMMANDS = {
		'create': create_message,
		'list': message_list
	}

	def get_command_code(self, data):
		initial = data.find('/') + 1
		data = data[initial:]
		data_splited = data.split('=')
		if len(data_splited) > 1:
			return data_splited[0].strip(), data_splited[1].strip()
		return data_splited[0].strip(), ''

	async def send_message(self, message):
		# Send message to room group
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'chat.message',
				'command': 'create',
				'message': message
			}
		)
