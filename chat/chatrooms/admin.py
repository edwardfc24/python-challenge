from django.contrib import admin


# Register your models here.
from chatrooms.models import Chatroom, User


class ChatroomAdmin(admin.ModelAdmin):
	pass


admin.site.register(Chatroom, ChatroomAdmin)


class UserAdmin(admin.ModelAdmin):
	pass


admin.site.register(User, UserAdmin)