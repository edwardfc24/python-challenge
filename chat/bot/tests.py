from django.test import TestCase

# Create your tests here.
from bot.services import BotService
from chatrooms.models import Chatroom


class BotTestCase(TestCase):


	def test_bot_with_correct_data(self):
		bot = BotService()
		room = Chatroom.objects.filter(name='main').first()
		good_command = 'stock'
		good_code = 'aapl.us'
		responses = {
			'good_response': 'AAPL.US quote is 315.01 per share',
			'bad_response': 'NOTHING quote is not defined',
			'bad_command_response': 'The command entered is not valid',
		}
		response = bot.bot_response(room, good_command, good_code)
		self.assertEqual(response[0]['content'], responses['good_response'])

	def test_bot_with_bad_data(self):
		bot = BotService()
		room = Chatroom.objects.filter(name='main').first()
		good_command = 'stock'
		bad_code = 'nothing'
		responses = {
			'good_response': 'AAPL.US quote is 315.01 per share',
			'bad_response': 'NOTHING quote is not defined',
			'bad_command_response': 'The command entered is not valid',
		}
		response = bot.bot_response(room, good_command, bad_code)
		self.assertEqual(response[0]['content'], responses['bad_response'])

	def test_bot_with_bad_command(self):
		bot = BotService()
		room = Chatroom.objects.filter(name='main').first()
		bad_command = 'other'
		bad_code = 'nothing'
		responses = {
			'good_response': 'AAPL.US quote is 315.01 per share',
			'bad_response': 'NOTHING quote is not defined',
			'bad_command_response': 'The command entered is not valid',
		}
		response = bot.bot_response(room, bad_command, bad_code)
		self.assertEqual(response[0]['content'], responses['bad_command_response'])
