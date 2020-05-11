from django.urls import path

from chatrooms.views import chatroom_view

app_name = 'chatroom'

urlpatterns = [
    path('', chatroom_view.lobby, name='lobby'),
    path('<str:name>/', chatroom_view.room, name='room'),
]
