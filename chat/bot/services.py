"""
Manage the API	Request for stock
"""
import csv
import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.contrib.sites import requests

from base.repositories.message_repository import MessageRepository
from chatrooms.models import User


class BotService:

	def __init__(self):
		self.base_url = 'https://stooq.com/q/l/?s='
		self.url_params = '&f=sd2t2ohlcv&h&e=csv'
		# Add more commands to avoid restrictions
		self.enable_commands = ['stock', ]
		# Enable the Message Repository
		self.message_repository = MessageRepository()

	def get_api_response(self, command, value):
		url = self.base_url + command + self.url_params
		response = requests.get(url)
		# Validate the status response
		if response.status == 200:
			file_stream = response.content.decode('utf-8')
			stock_data = csv.reader(file_stream.splitlines(), delimiter=',').next()
			# Header o file Symbol,Date,Time,Open,High,Low,Close,Volume
			# Find the value in header
			value_index = [i for i, head in range(stock_data[0]) if head == value]
			status = 'Success'
			if value_index:
				return_value = stock_data[1][value_index[0]]
			else:
				# By default return the Close value
				return_value = stock_data[1][6]
		else:
			status = 'Error'
			return_value = None
		return {
			'status': status,
			'value': return_value
		}

	def bot_response(self, chatroom, command, stock_code, save_response=False):
		# Validate if command is valid
		if command in self.enable_commands:
			response = self.get_api_response(stock_code, 'Close')
			if response['status'] == 'Success':
				# Prepare the data in correct format
				data = f"{ stock_code.upper() } quote is { response['value'] } per share"
			else:
				data = 'Stock code not found'
		else:
			data = 'The command entered is not valid'
		# Search the author marked as bot
		bot = User.objects.filter(is_bot=True).first()
		if not bot:
			bot = User.objects.create(
				username='stockBot',
				name='Stock',
				lastname='Bot',
				email='bot@fake.com',
				password='123456789'
			)
		message = self.message_repository.create_message(chatroom, bot, data, save_response)
		# Send the message to channel group
		channel_layer = get_channel_layer()
		async_to_sync(channel_layer.group_send)(
			chatroom.name,
			{
				'type': 'bot.message',
				'message': message
			})
