"""
Manage the message creation and serialization for use in channels
"""
from datetime import datetime

from asgiref.sync import sync_to_async

from chatrooms.models import Message


class MessageRepository:

	def serialize_message(self, package, many=False):
		items = []
		if many:
			for message in package:
				items.append({
					'id': message.id,
					'author': message.author.username,
					'author_fullname': f"{message.author.name} {message.author.lastname}",
					'formatted_time': message.created_at.strftime("%m/%d/%Y at %H:%M:%S"),
					'content': message.content
				})
		else:
			items.append({
				'id': package.id,
				'author': package.author.username,
				'author_fullname': f"{package.author.name} {package.author.lastname}",
				'formatted_time': package.created_at.strftime("%m/%d/%Y at %H:%M:%S"),
				'content': package.content
			})
		return items

	def create_message(self, chatroom, author, data, save_response=True):
		if save_response:
			message = Message.objects.create(
				chatroom=chatroom,
				author=author,
				content=data
			)
		else:
			message = Message()
			message.id = 0
			message.chatroom = chatroom
			message.author = author
			message.content = data
			message.created_at = datetime.now()
		return self.serialize_message(message)

	@sync_to_async
	def get_last_messages_for_room(self, chatroom, qty=50):
		messages = Message.objects.filter(chatroom__name=chatroom).order_by('-created_at')[:qty]
		return self.serialize_message(messages, True)

	@sync_to_async
	def get_last_messages_for_author(self, author, qty=50):
		messages = Message.objects.filter(author=author).order_by('-created_at')[:qty]
		return self.serialize_message(messages, True)
