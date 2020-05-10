from django.db import models

# Create your models here
from base.models import BaseModel


class Chatroom(BaseModel):

	name = models.CharField(max_length=150)
	description = models.TextField(null=True, blank=True)
