from django.db import models

# Create your models here
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	"""
	Use the Django Abstract user and add an attribute for bot
	"""
	is_bot = models.BooleanField(default=False)
