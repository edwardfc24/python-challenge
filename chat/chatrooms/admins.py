from django.contrib import admin


# Register your models here.
from chatrooms.models import Chatroom


class ChatroomAdmin(admin.ModelAdmin):
	pass


admin.site.register(Chatroom, ChatroomAdmin)
