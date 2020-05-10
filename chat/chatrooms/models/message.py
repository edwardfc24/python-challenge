from django.db import models

# Create your models here
from base.models import BaseModel
from chatrooms.models import User, Chatroom


class Message(BaseModel):

	content = models.TextField()
	autor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='messages')
	chatroom = models.ForeignKey(Chatroom, on_delete=models.PROTECT, related_name='messages')

